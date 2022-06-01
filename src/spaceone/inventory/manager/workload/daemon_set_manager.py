import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.workload.daemonset import DaemonSetConnector
from spaceone.inventory.model.workload.daemonset.cloud_service import DaemonSetResource, DaemonSetResponse
from spaceone.inventory.model.workload.daemonset.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.workload.daemonset.data import DaemonSet

_LOGGER = logging.getLogger(__name__)


class DaemonSetManager(KubernetesManager):
    connector_name = 'DaemonSetConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** DaemonSet Start **')
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
        pod_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        pod_conn: DaemonSetConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_daemon_set = pod_conn.list_daemon_set()
        #_LOGGER.debug(f'list_all_deployment => {list_all_deployment}')

        for daemon_set in list_all_daemon_set:
            try:
                #_LOGGER.debug(f'deployment => {deployment.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                daemon_set_name = daemon_set.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'daemon_set => {daemon_set}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = daemon_set.to_dict()
                raw_readonly = daemon_set.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['spec']['node_selector'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('node_selector', {}))
                raw_data['spec']['selector']['match_labels'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('selector', {}).get('match_labels', {}))
                raw_data['spec']['template']['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('metadata', {}).get('annotations', {}))
                raw_data['spec']['template']['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('metadata', {}).get('labels', {}))
                raw_data['spec']['template']['spec']['node_selector'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('spec', {}).get('node_selector', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                daemon_set_data = DaemonSet(raw_data, strict=False)
                _LOGGER.debug(f'deployment_data => {daemon_set_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                daemon_set_resource = DaemonSetResource({
                    'name': daemon_set_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': daemon_set_data,
                    'reference': daemon_set_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(DaemonSetResponse({'resource': daemon_set_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'WorkLoad', 'DaemonSet', pod_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

