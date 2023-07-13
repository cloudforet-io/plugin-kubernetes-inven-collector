import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.storage.persistent_volume_claim import (
    PersistentVolumeClaimConnector,
)
from spaceone.inventory.model.storage.persistent_volume_claim.cloud_service import (
    PersistentVolumeClaimResource,
    PersistentVolumeClaimResponse,
)
from spaceone.inventory.model.storage.persistent_volume_claim.cloud_service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.model.storage.persistent_volume_claim.data import (
    PersistentVolumeClaim,
)

_LOGGER = logging.getLogger(__name__)


class PersistentVolumeClaimManager(KubernetesManager):
    connector_name = "PersistentVolumeClaimConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f"** Persistent Volume Claim Start **")
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
        pvc_name = ""

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        pvc_conn: PersistentVolumeClaimConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        list_all_pvc = pvc_conn.list_persistent_volume_claim()
        # _LOGGER.debug(f'list_all_pvc => {list_all_pvc}')

        for pvc in list_all_pvc:
            try:
                # _LOGGER.debug(f'pvc => {pvc.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                pvc_name = pvc.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = "global"

                # _LOGGER.debug(f'pvc => {pvc}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = pvc.to_dict()
                raw_readonly = pvc.to_dict()
                raw_data["metadata"]["annotations"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("annotations", {})
                )
                raw_data["metadata"]["labels"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("labels", {})
                )
                raw_data["uid"] = raw_readonly["metadata"]["uid"]

                labels = raw_data["metadata"]["labels"]

                pvc_data = PersistentVolumeClaim(raw_data, strict=False)
                _LOGGER.debug(f"pvc_data => {pvc_data.to_primitive()}")

                ##################################
                # 3. Make Return Resource
                ##################################
                pvc_resource = PersistentVolumeClaimResource(
                    {
                        "name": pvc_name,
                        "account": cluster_name,
                        "tags": labels,
                        "region_code": region,
                        "data": pvc_data,
                        "reference": pvc_data.reference(),
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
                    PersistentVolumeClaimResponse({"resource": pvc_resource})
                )

            except Exception as e:
                _LOGGER.error(f"[collect_cloud_service] => {e}", exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(
                    e, "Storage", "PersistentVolumeClaim", pvc_name
                )
                error_responses.append(error_response)

        return collected_cloud_services, error_responses
