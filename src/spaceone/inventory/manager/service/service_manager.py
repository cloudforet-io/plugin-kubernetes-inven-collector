import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.service.service import ServiceConnector
from spaceone.inventory.model.service.service.cloud_service import (
    ServiceResource,
    ServiceResponse,
)
from spaceone.inventory.model.service.service.cloud_service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.model.service.service.data import Service

_LOGGER = logging.getLogger(__name__)


class ServiceManager(KubernetesManager):
    connector_name = "ServiceConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f"** Service Start **")
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
        service_name = ""

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        service_conn: ServiceConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        list_all_service = service_conn.list_service()
        # _LOGGER.debug(f'list_all_deployment => {list_all_deployment}')

        for service in list_all_service:
            try:
                # _LOGGER.debug(f'deployment => {deployment.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                service_name = service.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = "global"

                # _LOGGER.debug(f'service => {service}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = service.to_dict()
                raw_readonly = service.to_dict()
                raw_data["metadata"]["annotations"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("annotations", {})
                )
                raw_data["metadata"]["labels"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("labels", {})
                )
                raw_data["spec"]["selector"] = self.convert_labels_format(
                    raw_readonly.get("spec", {}).get("selector", {})
                )
                raw_data["uid"] = raw_readonly["metadata"]["uid"]

                labels = raw_data["metadata"]["labels"]

                service_data = Service(raw_data, strict=False)
                # _LOGGER.debug(f'service_data => {service_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                service_resource = ServiceResource(
                    {
                        "name": service_name,
                        "account": cluster_name,
                        "tags": labels,
                        "region_code": region,
                        "data": service_data,
                        "reference": service_data.reference(),
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
                    ServiceResponse({"resource": service_resource})
                )

            except Exception as e:
                _LOGGER.error(f"[collect_cloud_service] => {e}", exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(
                    e, "Service", "Service", service_name
                )
                error_responses.append(error_response)

        return collected_cloud_services, error_responses
