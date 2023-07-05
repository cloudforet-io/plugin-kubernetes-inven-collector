import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.workload.pod import PodConnector
from spaceone.inventory.model.workload.pod.cloud_service import PodResponse, PodResource
from spaceone.inventory.model.workload.pod.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.workload.pod.data import Pod

_LOGGER = logging.getLogger(__name__)


class PodManager(KubernetesManager):
    connector_name = 'PodConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** POD Start **')
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
        pod_conn: PodConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_pod = pod_conn.list_pod()
        #_LOGGER.debug(f'list_all_pod => {list_all_pod}')

        for pod in list_all_pod:
            try:
                #_LOGGER.debug(f'pod => {pod.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                pod_name = pod.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'


                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                raw_data = pod.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(raw_data.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(raw_data.get('metadata', {}).get('labels', {}))
                raw_data['spec']['node_selector'] = self.convert_labels_format(raw_data.get('spec', {}).get('node_selector', {}))
                raw_data['uid'] = raw_data['metadata']['uid']
                raw_data['restarts'] = self._get_restarts(raw_data.get('status', {}).get('container_statuses', []))
                raw_data['age'] = self.get_age(raw_data.get('metadata', {}).get('creation_timestamp', ''))
                raw_data['containers'] = self.get_containers(raw_data.get('status', {}).get('container_statuses', []),
                                                             raw_data.get('spec', {}).get('containers', []))

                labels = raw_data['metadata']['labels']

                pod_data = Pod(raw_data, strict=False)
                #_LOGGER.debug(f'pod_data => {pod_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                pod_resource = PodResource({
                    'name': pod_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': pod_data,
                    'reference': pod_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(PodResponse({'resource': pod_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'WorkLoad', 'Pod', pod_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

    @staticmethod
    def _get_restarts(container_statuses):
        if container_statuses is None:
            container_statuses = []
        if len(container_statuses) >= 1:
            restarts = container_statuses[0].get('restart_count', 0)
        else:
            restarts = 0
        return restarts

