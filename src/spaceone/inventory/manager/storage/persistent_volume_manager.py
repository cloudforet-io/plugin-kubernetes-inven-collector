import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.storage.persistent_volume import PersistentVolumeConnector
from spaceone.inventory.model.storage.persistent_volume.cloud_service import PersistentVolumeResource, \
    PersistentVolumeResponse
from spaceone.inventory.model.storage.persistent_volume.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.storage.persistent_volume.data import PersistentVolume

_LOGGER = logging.getLogger(__name__)


class PersistentVolumeManager(KubernetesManager):
    connector_name = 'PersistentVolumeConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Persistent Volume Start **')
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

        secret_data = params['secret_data']
        persistent_volume_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        persistent_volume_conn: PersistentVolumeConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_persistent_volume = persistent_volume_conn.list_persistent_volume()
        #_LOGGER.debug(f'list_all_persistent_volume => {list_all_persistent_volume}')

        for persistent_volume in list_all_persistent_volume:
            try:
                #_LOGGER.debug(f'persistent_volume => {persistent_volume.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                persistent_volume_name = persistent_volume.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                _LOGGER.debug(f'persistent_volume => {persistent_volume}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = persistent_volume.to_dict()
                raw_readonly = persistent_volume.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                labels = raw_data['metadata']['labels']

                persistent_volume_data = PersistentVolume(raw_data, strict=False)
                _LOGGER.debug(f'persistent_volume_data => {persistent_volume_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                persistent_volume_resource = PersistentVolumeResource({
                    'name': persistent_volume_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': persistent_volume_data,
                    'reference': persistent_volume_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(PersistentVolumeResponse({'resource': persistent_volume_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Storage', 'PersistentVolume', persistent_volume_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

