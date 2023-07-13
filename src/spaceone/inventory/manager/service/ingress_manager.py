import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.service.ingress import IngressConnector
from spaceone.inventory.model.service.ingress.cloud_service import (
    IngressResource,
    IngressResponse,
)
from spaceone.inventory.model.service.ingress.cloud_service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.model.service.ingress.data import Ingress

_LOGGER = logging.getLogger(__name__)


class IngressManager(KubernetesManager):
    connector_name = "IngressConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f"** Ingress Start **")
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
        ingress_name = ""

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        ingress_conn: IngressConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        list_all_ingress = ingress_conn.list_ingress()
        # _LOGGER.debug(f'list_all_ingress => {list_all_ingress}')

        for ingress in list_all_ingress:
            try:
                # _LOGGER.debug(f'ingress => {ingress.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                ingress_name = ingress.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = "global"

                # _LOGGER.debug(f'ingress => {ingress}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = ingress.to_dict()
                raw_readonly = ingress.to_dict()
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

                ingress_data = Ingress(raw_data, strict=False)
                _LOGGER.debug(f"ingress_data => {ingress_data.to_primitive()}")

                ##################################
                # 3. Make Return Resource
                ##################################
                ingress_resource = IngressResource(
                    {
                        "name": ingress_name,
                        "account": cluster_name,
                        "tags": labels,
                        "region_code": region,
                        "data": ingress_data,
                        "reference": ingress_data.reference(),
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
                    IngressResponse({"resource": ingress_resource})
                )

            except Exception as e:
                _LOGGER.error(f"[collect_cloud_service] => {e}", exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(
                    e, "Service", "Ingress", ingress_name
                )
                error_responses.append(error_response)

        return collected_cloud_services, error_responses
