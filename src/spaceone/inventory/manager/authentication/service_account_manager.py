import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.authentication.service_account import (
    ServiceAccountConnector,
)
from spaceone.inventory.model.authentication.service_account.cloud_service import (
    ServiceAccountResource,
    ServiceAccountResponse,
)
from spaceone.inventory.model.authentication.service_account.cloud_service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.model.authentication.service_account.data import ServiceAccount

_LOGGER = logging.getLogger(__name__)


class ServiceAccountManager(KubernetesManager):
    connector_name = "ServiceAccountConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f"** Service Account Start **")
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
        service_account_name = ""

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        service_account_conn: ServiceAccountConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        list_all_service_account = service_account_conn.list_service_account()
        # _LOGGER.debug(f'list_all_service_account => {list_all_service_account}')

        for service_account in list_all_service_account:
            try:
                # _LOGGER.debug(f'service_account => {service_account.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                service_account_name = service_account.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = "global"

                # _LOGGER.debug(f'service_account => {service_account}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = service_account.to_dict()
                raw_readonly = service_account.to_dict()
                raw_data["metadata"]["annotations"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("annotations", {})
                )
                raw_data["metadata"]["labels"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("labels", {})
                )
                raw_data["uid"] = raw_readonly["metadata"]["uid"]

                labels = raw_data["metadata"]["labels"]

                service_account_data = ServiceAccount(raw_data, strict=False)
                _LOGGER.debug(
                    f"service_account_data => {service_account_data.to_primitive()}"
                )

                ##################################
                # 3. Make Return Resource
                ##################################
                service_account_resource = ServiceAccountResource(
                    {
                        "name": service_account_name,
                        "account": cluster_name,
                        "tags": labels,
                        "region_code": region,
                        "data": service_account_data,
                        "reference": service_account_data.reference(),
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
                    ServiceAccountResponse({"resource": service_account_resource})
                )

            except Exception as e:
                _LOGGER.error(f"[collect_cloud_service] => {e}", exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(
                    e, "Authentication", "ServiceAccount", service_account_name
                )
                error_responses.append(error_response)

        return collected_cloud_services, error_responses
