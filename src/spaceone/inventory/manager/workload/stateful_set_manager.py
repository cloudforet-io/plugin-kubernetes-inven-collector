import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.workload.statefulset import StatefulSetConnector
from spaceone.inventory.model.workload.statefulset.cloud_service import StatefulSetResource, StatefulSetResponse
from spaceone.inventory.model.workload.statefulset.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.workload.statefulset.data import StatefulSet

_LOGGER = logging.getLogger(__name__)


class StatefulSetManager(KubernetesManager):
    connector_name = 'StatefulSetConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** StatefulSet Start **')
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
        stateful_set_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        stateful_set_conn: StatefulSetConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_stateful_set = stateful_set_conn.list_stateful_set()
        #_LOGGER.debug(f'list_all_stateful_set => {list_all_stateful_set}')
        list_all_pod = stateful_set_conn.list_pod()
        # _LOGGER.debug(f'list_all_pod => {list_all_pod}')

        for stateful_set in list_all_stateful_set:
            try:
                #_LOGGER.debug(f'stateful_set => {stateful_set.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                stateful_set_name = stateful_set.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'stateful_set => {stateful_set}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = stateful_set.to_dict()
                raw_readonly = stateful_set.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(raw_readonly.get('metadata', {}).get('labels', {}))

                raw_data['spec']['selector'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('selector', {}))

                raw_data['spec']['template']['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('metadata', {}).get('annotations', {}))
                raw_data['spec']['template']['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('metadata', {}).get('labels', {}))
                raw_data['spec']['template']['spec']['node_selector'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('spec', {}).get('node_selector', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']
                raw_data['age'] = self.get_age(raw_readonly.get('metadata', {}).get('creation_timestamp', ''))
                raw_data['pods'] = self._get_pods(list_all_pod, raw_readonly.get('metadata', {}).get('uid', ''))

                labels = raw_data['metadata']['labels']

                raw_data['uid'] = raw_readonly['metadata']['uid']

                stateful_set_data = StatefulSet(raw_data, strict=False)
                #_LOGGER.debug(f'stateful_set_data => {stateful_set_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                stateful_set_resource = StatefulSetResource({
                    'name': stateful_set_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': stateful_set_data,
                    'reference': stateful_set_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(StatefulSetResponse({'resource': stateful_set_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'WorkLoad', 'StatefulSet', stateful_set_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

    def _get_pods(self, list_pods, stateful_set_uid):
        pods_for_stateful_set = []
        for pod in list_pods:
            raw_pod = pod.to_dict()
            pod_owner_reference = raw_pod.get('metadata', {}).get('owner_references', [])[0]
            if stateful_set_uid == pod_owner_reference.get('uid', ''):
                matched_pod = self._convert_pod_data(pod)
                pods_for_stateful_set.append(matched_pod)
        return pods_for_stateful_set
