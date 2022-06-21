import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.authorization.role import RoleConnector
from spaceone.inventory.model.authorization.role.cloud_service import RoleResource, RoleResponse
from spaceone.inventory.model.authorization.role.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.authorization.role.data import Role

_LOGGER = logging.getLogger(__name__)


class RoleManager(KubernetesManager):
    connector_name = 'RoleConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Role Start **')
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
        role_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        role_conn: RoleConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_role = role_conn.list_role()
        #_LOGGER.debug(f'list_all_role => {list_all_role}')

        for role in list_all_role:
            try:
                #_LOGGER.debug(f'role => {role.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                role_name = role.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'role => {role}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = role.to_dict()
                raw_readonly = role.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                labels = raw_data['metadata']['labels']

                role_data = Role(raw_data, strict=False)
                #_LOGGER.debug(f'role_data => {role_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                role_resource = RoleResource({
                    'name': role_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': role_data,
                    'reference': role_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(RoleResponse({'resource': role_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Authorization', 'Role', role_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

