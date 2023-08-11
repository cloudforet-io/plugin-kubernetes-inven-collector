import logging

from spaceone.inventory.connector.workload.job import JobConnector
from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.model.workload.job.cloud_service import JobResponse, JobResource
from spaceone.inventory.model.workload.job.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.workload.job.data import Job

_LOGGER = logging.getLogger(__name__)


class JobManager(KubernetesManager):
    connector_name = "JobConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug("** Job Start **")
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        collected_cloud_services = []
        error_responses = []

        secret_data = params["secret_data"]
        pod_name = ""

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        pod_conn: JobConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        list_all_job = pod_conn.list_job()
        list_all_pod = pod_conn.list_pod()

        for job in list_all_job:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                job_name = job.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = "global"

                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = job.to_dict()
                raw_readonly = job.to_dict()
                raw_data["metadata"]["annotations"] = self.convert_labels_format(
                    raw_data.get("metadata", {}).get("annotations", {})
                )
                raw_data["metadata"]["labels"] = self.convert_labels_format(
                    raw_data.get("metadata", {}).get("labels", {})
                )
                raw_data["spec"]["node_selector"] = self.convert_labels_format(
                    raw_data.get("spec", {}).get("node_selector", {})
                )
                raw_data["spec"]["selector"][
                    "match_labels"
                ] = self.convert_labels_format(
                    raw_data.get("spec", {}).get("selector", {}).get("match_labels", {})
                )

                raw_data["spec"]["template"]["metadata"][
                    "annotations"
                ] = self.convert_labels_format(
                    raw_readonly.get("spec", {})
                    .get("template", {})
                    .get("metadata", {})
                    .get("annotations", {})
                )
                raw_data["spec"]["template"]["metadata"][
                    "labels"
                ] = self.convert_labels_format(
                    raw_readonly.get("spec", {})
                    .get("template", {})
                    .get("metadata", {})
                    .get("labels", {})
                )
                raw_data["spec"]["template"]["spec"][
                    "node_selector"
                ] = self.convert_labels_format(
                    raw_readonly.get("spec", {})
                    .get("template", {})
                    .get("spec", {})
                    .get("node_selector", {})
                )
                raw_data["uid"] = raw_readonly.get("metadata", {}).get("uid", "")
                raw_data["completions"] = self._get_completion(
                    raw_readonly.get("status", {})
                )
                raw_data["age"] = self.get_age(
                    raw_readonly.get("metadata", {}).get("creation_timestamp", "")
                )
                raw_data["pods"] = self._get_pods(
                    list_all_pod,
                    raw_readonly.get("metadata", {}).get("uid", ""),
                )

                labels = raw_data["metadata"]["labels"]

                job_data = Job(raw_data, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                pod_resource = JobResource(
                    {
                        "name": job_name,
                        "account": cluster_name,
                        "tags": labels,
                        "region_code": region,
                        "data": job_data,
                        "reference": job_data.reference(),
                    }
                )

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(JobResponse({"resource": pod_resource}))

            except Exception as e:
                _LOGGER.error(f"[collect_cloud_service] => {e}", exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(
                    e, "WorkLoad", "Job", pod_name
                )
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

    @staticmethod
    def _get_completion(status):
        if not status:
            status = {}

        completion = (
            # TODO: Need to logic check
            str(status.get("succeeded", 0))
            + "/"
            + str(status.get("succeeded", 0))
        )

        return completion

    def _get_pods(self, list_pods, job_uid):
        pods_for_job = []
        for pod in list_pods:
            raw_pod = pod.to_dict()
            if raw_pod.get("metadata").get("owner_references") is None:
                continue

            pod_owner_reference = raw_pod.get("metadata", {}).get(
                "owner_references", []
            )[0]
            if job_uid == pod_owner_reference.get("uid", ""):
                matched_pod = self._convert_pod_data(pod)
                pods_for_job.append(matched_pod)
        return pods_for_job
