import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.application.custom_resource_definition import CustomResourceDefinitionConnector
from spaceone.inventory.model.application.custom_resource_definition.cloud_service import CustomResourceDefinitionResource, \
    CustomResourceDefinitionResourceResponse
from spaceone.inventory.model.application.custom_resource_definition.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.application.custom_resource_definition.data import CustomResourceDefinition

_LOGGER = logging.getLogger(__name__)


class CustomResourceDefinitionManager(KubernetesManager):
    connector_name = 'CustomResourceDefinitionConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Custom Resource Definition Start **')
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
        crd_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        crd_conn: CustomResourceDefinitionConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_crd = crd_conn.list_custom_resource_definition()
        #_LOGGER.debug(f'list_all_crd => {list_all_crd}')

        for crd in list_all_crd:
            try:
                #_LOGGER.debug(f'crd => {crd.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                crd_name = crd.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'crd => {crd}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = crd.to_dict()
                raw_readonly = crd.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                crd_data = CustomResourceDefinition(raw_data, strict=False)
                _LOGGER.debug(f'crd_data => {crd_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                crd_resource = CustomResourceDefinitionResource({
                    'name': crd_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': crd_data,
                    'reference': crd_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(CustomResourceDefinitionResourceResponse({'resource': crd_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Application', 'CustomResourceResponse', crd_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

