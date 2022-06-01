import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.config.secret import SecretConnector
from spaceone.inventory.model.config.secret.cloud_service import SecretResource, SecretResponse
from spaceone.inventory.model.config.secret.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.config.secret.data import Secret

_LOGGER = logging.getLogger(__name__)


class SecretManager(KubernetesManager):
    connector_name = 'SecretConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Secret Start **')
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
        secret_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        secret_conn: SecretConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_secret = secret_conn.list_secret()
        #_LOGGER.debug(f'list_all_secret => {list_all_secret}')

        for secret in list_all_secret:
            try:
                #_LOGGER.debug(f'secret => {secret.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                secret_name = secret.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                _LOGGER.debug(f'secret => {secret}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = secret.to_dict()
                raw_readonly = secret.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                secret_data = Secret(raw_data, strict=False)
                _LOGGER.debug(f'secret => {secret_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                secret_resource = SecretResource({
                    'name': secret_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': secret_data,
                    'reference': secret_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(SecretResponse({'resource': secret_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Config', 'Secret', secret_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

