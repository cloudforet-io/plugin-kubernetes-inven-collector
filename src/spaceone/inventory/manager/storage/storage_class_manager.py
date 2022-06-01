import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.storage.storage_class import StorageClassConnector
from spaceone.inventory.model.storage.storage_class.cloud_service import StorageClassResource, StorageClassResponse
from spaceone.inventory.model.storage.storage_class.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.storage.storage_class.data import StorageClass

_LOGGER = logging.getLogger(__name__)


class StorageClassManager(KubernetesManager):
    connector_name = 'StorageClassConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Storage Class Start **')
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
        storage_class_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        storage_class_conn: StorageClassConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_storage_class = storage_class_conn.list_storage_class()
        #_LOGGER.debug(f'list_all_storage_class => {list_all_storage_class}')

        for storage_class in list_all_storage_class:
            try:
                #_LOGGER.debug(f'storage_class => {storage_class.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                storage_class_name = storage_class.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'storage_class => {storage_class}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = storage_class.to_dict()
                raw_readonly = storage_class.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                storage_class_data = StorageClass(raw_data, strict=False)
                _LOGGER.debug(f'storage_class_data => {storage_class_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                storage_class_resource = StorageClassResource({
                    'name': storage_class_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': storage_class_data,
                    'reference': storage_class_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(StorageClassResponse({'resource': storage_class_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Storage', 'StorageClass', storage_class_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

