import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.service.network_policy import NetworkPolicyConnector
from spaceone.inventory.model.service.network_policy.cloud_service import NetworkPolicyResource, NetworkPolicyResponse
from spaceone.inventory.model.service.network_policy.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.service.network_policy.data import NetworkPolicy

_LOGGER = logging.getLogger(__name__)


class NetworkPolicyManager(KubernetesManager):
    connector_name = 'NetworkPolicyConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Network Policy Start **')
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
        network_policy_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        network_policy_conn: NetworkPolicyConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_network_policy = network_policy_conn.list_network_policy()
        #_LOGGER.debug(f'list_all_network_policy => {list_all_network_policy}')

        for network_policy in list_all_network_policy:
            try:
                _LOGGER.debug(f'network_policy => {network_policy.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                network_policy_name = network_policy.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = network_policy.to_dict()
                raw_readonly = network_policy.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['spec']['pod_selector'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('pod_selector', {}))
                raw_data['ingress']['from']['namespace_selector'] = self.convert_labels_format(
                    raw_readonly.get('ingress', {}).get('from', {}).get('namespace_selector', {})
                )
                raw_data['ingress']['from']['pod_selector'] = self.convert_labels_format(
                    raw_readonly.get('ingress', {}).get('from', {}).get('pod_selector', {})
                )
                raw_data['egress']['to']['namespace_selector'] = self.convert_labels_format(
                    raw_readonly.get('egress', {}).get('to', {}).get('namespace_selector', {})
                )
                raw_data['egress']['to']['pod_selector'] = self.convert_labels_format(
                    raw_readonly.get('egress', {}).get('to', {}).get('pod_selector', {})
                )
                raw_data['uid'] = raw_readonly['metadata']['uid']

                network_policy_data = NetworkPolicy(raw_data, strict=False)
                _LOGGER.debug(f'network_policy_data => {network_policy_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                network_policy_resource = NetworkPolicyResource({
                    'name': network_policy_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': network_policy_data,
                    'reference': network_policy_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(NetworkPolicyResponse({'resource': network_policy_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Service', 'NetworkPolicy', network_policy_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

