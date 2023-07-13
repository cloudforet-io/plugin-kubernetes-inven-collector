import json
import logging
from datetime import datetime, timezone

from spaceone.core.manager import BaseManager

from spaceone.inventory.conf.cloud_service_conf import REGION_INFO
from spaceone.inventory.libs.connector import KubernetesConnector
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse

_LOGGER = logging.getLogger(__name__)


class KubernetesManager(BaseManager):
    connector_name = None
    cloud_service_types = []
    response_schema = None
    collected_region_codes = []

    def verify(self, options, secret_data, **kwargs):
        """Check collector's status."""
        connector: KubernetesConnector = KubernetesConnector(secret_data=secret_data)
        connector.verify()

    def collect_cloud_service_type(self, params):
        options = params.get("options", {})

        for cloud_service_type in self.cloud_service_types:
            if "service_code_mappers" in options:
                svc_code_maps = options["service_code_mappers"]
                if (
                    getattr(cloud_service_type.resource, "service_code")
                    and cloud_service_type.resource.service_code in svc_code_maps
                ):
                    cloud_service_type.resource.service_code = svc_code_maps[
                        cloud_service_type.resource.service_code
                    ]
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        total_resources = []

        try:
            # Collect Cloud Service Type
            total_resources.extend(self.collect_cloud_service_type(params))

            # Collect Cloud Service
            resources, error_resources = self.collect_cloud_service(params)
            total_resources.extend(resources)
            total_resources.extend(error_resources)

            # Collect Region
            total_resources.extend(self.collect_region())

        except Exception as e:
            _LOGGER.error(f"[collect_resources] {e}", exc_info=True)
            error_resource_response = self.generate_error_response(
                e,
                self.cloud_service_types[0].resource.group,
                self.cloud_service_types[0].resource.name,
            )
            total_resources.append(error_resource_response)

        return total_resources

    def collect_region(self):
        results = []
        for region_code in self.collected_region_codes:
            if region := self.match_region_info(region_code):
                results.append(RegionResponse({"resource": region}))

        return results

    def set_region_code(self, region):
        if region not in REGION_INFO:
            region = "global"

        if region not in self.collected_region_codes:
            self.collected_region_codes.append(region)

    def get_kubernetes_provider(self, list_node):
        kubernetes_provider = "unknown"
        if len(list_node) > 0:
            node = list_node[0]
            raw_node = node.to_dict()
            provider_id = raw_node.get("spec", {}).get("provider_id", "")
            if provider_id is None or provider_id == "":
                kubernetes_provider = self.get_provider_from_node(raw_node)
            else:
                kubernetes_provider = self.get_provider_from_provider_id(provider_id)
        else:
            kubernetes_provider = "unknown"

        return kubernetes_provider

    def get_kubernetes_version(self, list_node):
        kubernetes_version = "unknown"
        if len(list_node) > 0:
            node = list_node[0]
            raw_node = node.to_dict()
            kubernetes_version = self.get_version_from_node(raw_node)
        else:
            kubernetes_version = "unknown"

        return kubernetes_version

    @staticmethod
    def get_memory_total_per_node(node):
        # "memory": "1003292Ki"
        raw_node = node.to_dict()
        memory = raw_node.get("status", {}).get("allocatable", {}).get("memory", "0Ki")

        return memory

    @staticmethod
    def get_cpu_total_per_node(node):
        # "cpu": "940m"
        raw_node = node.to_dict()
        cpu = raw_node.get("status", {}).get("allocatable", {}).get("cpu", "0m")

        return cpu

    @staticmethod
    def get_pod_count_total_per_node(node):
        # "pods": "110"
        raw_node = node.to_dict()
        pod_count = raw_node.get("status", {}).get("allocatable", {}).get("pod", 0)

        return pod_count

    @staticmethod
    def get_cpu_current_per_node(node, list_pod):
        """
        get cpu current usage from resources.requests.cpus in each containers
        """
        cpu_current = ""
        node_name = node.to_dict().get("metadata", {}).get("name", "")
        for pod in list_pod:
            pod_raw = pod.to_dict()
            if node_name == pod_raw.get("spec", {}).get("node_name", ""):
                list_container = pod_raw.get("spec", {}).get("containers", "")
                for container in list_container:
                    log = container.get("resources", {})
                    _LOGGER.debug(f"requests => {log}")
                    cpu = (
                        container.get("resources", {})
                        .get("requests", {})
                        .get("cpu", "0m")
                    )
                    cpu_current = cpu_current + int(cpu.replace("m", ""))

        return cpu_current

    @staticmethod
    def convert_labels_format(labels):
        convert_labels = []
        if labels is not None:
            for k, v in labels.items():
                convert_labels.append({"key": k, "value": v})
        return convert_labels

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse(
                {
                    "message": json.dumps(e),
                    "resource": {
                        "cloud_service_group": cloud_service_group,
                        "cloud_service_type": cloud_service_type,
                    },
                }
            )
        else:
            error_resource_response = ErrorResourceResponse(
                {
                    "message": str(e),
                    "resource": {
                        "cloud_service_group": cloud_service_group,
                        "cloud_service_type": cloud_service_type,
                    },
                }
            )

        return error_resource_response

    @staticmethod
    def generate_resource_error_response(
        e, cloud_service_group, cloud_service_type, resource_id
    ):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse(
                {
                    "message": json.dumps(e),
                    "resource": {
                        "cloud_service_group": cloud_service_group,
                        "cloud_service_type": cloud_service_type,
                        "resource_id": resource_id,
                    },
                }
            )
        else:
            error_resource_response = ErrorResourceResponse(
                {
                    "message": str(e),
                    "resource": {
                        "cloud_service_group": cloud_service_group,
                        "cloud_service_type": cloud_service_type,
                        "resource_id": resource_id,
                    },
                }
            )
        return error_resource_response

    @staticmethod
    def match_region_info(region_code):
        match_region_info = REGION_INFO.get(region_code)

        if match_region_info:
            region_info = match_region_info.copy()
            region_info.update({"region_code": region_code})
            return RegionResource(region_info, strict=False)

        return None

    @staticmethod
    def get_cluster_name(secret_data):
        """
        Get cluster name from secret_data(kubeconfig)
        :param secret_data:
        :return:
        """
        cluster_name = secret_data.get("cluster_name", "")
        current_context = secret_data.get("current-context", "")
        list_contexts = secret_data.get("contexts", [])

        for context in list_contexts:
            if current_context == context.get("name", ""):
                cluster_name = context.get("context", {}).get("cluster", "")

        return cluster_name

    @staticmethod
    def get_provider_from_node(raw_node):
        kubelet_version = (
            raw_node.get("status", {}).get("node_info", {}).get("kubelet_version", "")
        )
        if len(kubelet_version.split("-")) >= 2:
            if kubelet_version.split("-")[1].startswith("gke"):
                return "gke"
            elif kubelet_version.split("-")[1].startswith("eks"):
                return "eks"
            else:
                return "unknown"
        else:
            return "unknown"

    @staticmethod
    def get_version_from_node(raw_node):
        kubelet_version = (
            raw_node.get("status", {}).get("node_info", {}).get("kubelet_version", "")
        )
        if len(kubelet_version.split("-")) >= 1:
            return kubelet_version.split("-")[0]
        else:
            return "unknown"

    @staticmethod
    def get_provider_from_provider_id(provider_id):
        """
        provider_id => aws:///ap-northeast-2c/i-xxxxxxxx
        :param provider_id:
        :return:
        """
        _LOGGER.debug(f"get_provider_from_provider_id => {provider_id}")
        cloud_provider = provider_id.split(":")[0]
        if cloud_provider == "aws":
            return "eks"
        elif cloud_provider == "gce":
            return "gke"
        else:
            return "unknown"

    def get_age(self, creation_timestamp):
        if creation_timestamp is None:
            creation_timestamp = datetime.now(timezone.utc)
        now = datetime.now(timezone.utc)
        delta = now - creation_timestamp
        age = str(delta)
        return age

    def get_containers(self, status_container_statuses, spec_containers):
        if spec_containers is None:
            spec_containers = []
        if status_container_statuses is None:
            status_container_statuses = []

        ready_container_count = 0
        for i in status_container_statuses:
            if i["ready"] == True:
                ready_container_count = ready_container_count + 1
        containers = str(ready_container_count) + "/" + str(len(spec_containers))
        return containers

    def _convert_pod_data(self, pod):
        raw_pod = pod.to_dict()
        raw_pod["metadata"]["annotations"] = self.convert_labels_format(
            raw_pod.get("metadata", {}).get("annotations", {})
        )
        raw_pod["metadata"]["labels"] = self.convert_labels_format(
            raw_pod.get("metadata", {}).get("labels", {})
        )
        raw_pod["spec"]["node_selector"] = self.convert_labels_format(
            raw_pod.get("spec", {}).get("node_selector", {})
        )
        raw_pod["uid"] = raw_pod["metadata"]["uid"]
        raw_pod["age"] = self.get_age(
            raw_pod.get("metadata", {}).get("creation_timestamp", "")
        )
        raw_pod["containers"] = self.get_containers(
            raw_pod.get("status", {}).get("container_statuses", []),
            raw_pod.get("spec", {}).get("containers", []),
        )
        return raw_pod

    def get_config_data_keys(self, config_data):
        keys = ""
        for k in config_data.keys():
            keys = k + "," + keys
        return keys
