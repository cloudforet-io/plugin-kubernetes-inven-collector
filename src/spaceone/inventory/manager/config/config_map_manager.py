import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.config.config_map import ConfigMapConnector
from spaceone.inventory.model.config.config_map.cloud_service import ConfigMapResource, ConfigMapResponse
from spaceone.inventory.model.config.config_map.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.config.config_map.data import ConfigMap

_LOGGER = logging.getLogger(__name__)


class ConfigMapManager(KubernetesManager):
    connector_name = 'ConfigMapConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Config Map Start **')
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
        config_map_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        config_map_conn: ConfigMapConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_config_map = config_map_conn.list_config_map()
        #_LOGGER.debug(f'list_all_config_map => {list_all_config_map}')

        for config_map in list_all_config_map:
            try:
                #_LOGGER.debug(f'config_map => {config_map.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                config_map_name = config_map.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'config_map => {config_map}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = config_map.to_dict()
                raw_readonly = config_map.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                config_map_data = ConfigMap(raw_data, strict=False)
                #_LOGGER.debug(f'config_map_data => {config_map_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                config_map_resource = ConfigMapResource({
                    'name': config_map_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': config_map_data,
                    'reference': config_map_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(ConfigMapResponse({'resource': config_map_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Config', 'ConfigMap', config_map_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

