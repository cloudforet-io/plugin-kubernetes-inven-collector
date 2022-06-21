import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.authorization.cluster_role import ClusterRoleConnector
from spaceone.inventory.model.authorization.cluster_role.cloud_service import ClusterRoleResource, ClusterRoleResponse
from spaceone.inventory.model.authorization.cluster_role.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.authorization.cluster_role.data import ClusterRole

_LOGGER = logging.getLogger(__name__)


class ClusterRoleManager(KubernetesManager):
    connector_name = 'ClusterRoleConnector'
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
        cluster_role_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        cluster_role_conn: ClusterRoleConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_cluster_role = cluster_role_conn.list_cluster_role()
        #_LOGGER.debug(f'list_all_cluster_role => {list_all_cluster_role}')

        for cluster_role in list_all_cluster_role:
            try:
                #_LOGGER.debug(f'cluster_role => {cluster_role.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                cluster_role_name = cluster_role.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                _LOGGER.debug(f'cluster_role => {cluster_role}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = cluster_role.to_dict()
                raw_readonly = cluster_role.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))

                labels = raw_data['metadata']['labels']

                # aggregation_rule can be null
                if raw_readonly.get('aggregation_rule', {}) is not None:
                    raw_data['aggregation_rule']['cluster_role_selectors'] = self._convert_cluster_role_selectors(
                        raw_readonly.get('aggregation_rule', {}).get('cluster_role_selectors', [])
                    )

                raw_data['uid'] = raw_readonly['metadata']['uid']

                cluster_role_data = ClusterRole(raw_data, strict=False)
                _LOGGER.debug(f'cluster_role_data => {cluster_role_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                cluster_role_resource = ClusterRoleResource({
                    'name': cluster_role_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': cluster_role_data,
                    'reference': cluster_role_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(ClusterRoleResponse({'resource': cluster_role_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Authorization', 'ClusterRole', cluster_role_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

    def _convert_cluster_role_selectors(self, origin_cluster_role_selectors) -> list:
        """
        Convert cluster_role_selector data type
        'cluster_role_selectors': ['match_labels': {'xxx': 'yyyy'}]
            -> 'cluster_role_selectors': ['match_labels': [{'key': 'xxx', 'value': 'yyyy'}]]
        :return:
        """
        convert_cluster_role_selectors = []

        for cluster_role_selector in origin_cluster_role_selectors:
            convert_cluster_role_selectors.append({
                'match_expressions': cluster_role_selector.get('match_expressions', None),
                'match_labels': self.convert_labels_format(
                    cluster_role_selector.get('match_labels', {})
                )
            })

        _LOGGER.debug(f'_convert_cluster_role_selectors => {convert_cluster_role_selectors}')
        return convert_cluster_role_selectors



