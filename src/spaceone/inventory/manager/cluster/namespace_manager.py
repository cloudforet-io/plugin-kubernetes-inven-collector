import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.cluster.namespace import NamespaceConnector
from spaceone.inventory.model.cluster.namespace.cloud_service import (
    NamespaceResource,
    NamespaceResponse,
)
from spaceone.inventory.model.cluster.namespace.cloud_service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.model.cluster.namespace.data import Namespace


_LOGGER = logging.getLogger(__name__)


class NamespaceManager(KubernetesManager):
    connector_name = "NamespaceConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f"** Namespace Start **")
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
        namespace_conn: NamespaceConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        list_all_namespace = namespace_conn.list_namespace()
        # _LOGGER.debug(f'list_all_deployment => {list_all_deployment}')

        for namespace in list_all_namespace:
            try:
                # _LOGGER.debug(f'deployment => {deployment.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                namespace_name = namespace.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = "global"

                # _LOGGER.debug(f'node => {node}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = namespace.to_dict()
                raw_readonly = namespace.to_dict()
                raw_data["metadata"]["annotations"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("annotations", {})
                )
                raw_data["metadata"]["labels"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("labels", {})
                )
                raw_data["uid"] = raw_readonly["metadata"]["uid"]

                labels = raw_data["metadata"]["labels"]

                namespace_data = Namespace(raw_data, strict=False)
                # _LOGGER.debug(f'namespace_data => {namespace_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                namespace_resource = NamespaceResource(
                    {
                        "name": namespace_name,
                        "account": cluster_name,
                        "tags": labels,
                        "region_code": region,
                        "data": namespace_data,
                        "reference": namespace_data.reference(),
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
                collected_cloud_services.append(
                    NamespaceResponse({"resource": namespace_resource})
                )

            except Exception as e:
                _LOGGER.error(f"[collect_cloud_service] => {e}", exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(
                    e, "WorkLoad", "Namespace", pod_name
                )
                error_responses.append(error_response)

        return collected_cloud_services, error_responses
