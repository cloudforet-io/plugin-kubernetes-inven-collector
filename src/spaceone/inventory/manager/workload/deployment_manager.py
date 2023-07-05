import logging
from datetime import datetime, timezone

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.workload.deployment import DeploymentConnector
from spaceone.inventory.model.workload.deployment.cloud_service import DeploymentResponse, DeploymentResource
from spaceone.inventory.model.workload.deployment.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.workload.deployment.data import Deployment

_LOGGER = logging.getLogger(__name__)


class DeploymentManager(KubernetesManager):
    connector_name = 'DeploymentConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Deployment Start **')
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
        pod_conn: DeploymentConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_deployment = pod_conn.list_deployment()
        #_LOGGER.debug(f'list_all_deployment => {list_all_deployment}')
        list_all_pod = pod_conn.list_pod()
        #_LOGGER.debug(f'list_all_pod => {list_all_pod}')
        list_all_replicaset = pod_conn.list_replicaset()
        #_LOGGER.debug(f'list_all_replicaset => {list_all_replicaset}')

        for deployment in list_all_deployment:
            try:
                # _LOGGER.debug(f'deployment => {deployment.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                deployment_name = deployment.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict

                raw_data = deployment.to_dict()
                raw_readonly = deployment.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_data.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_data.get('metadata', {}).get('labels', {}))

                raw_data['spec']['node_selector'] = self.convert_labels_format(
                    raw_data.get('spec', {}).get('node_selector', {}))
                raw_data['spec']['selector']['match_labels'] = self.convert_labels_format(
                    raw_data.get('spec', {}).get('selector', {}).get('match_labels', {}))

                raw_data['spec']['template']['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('metadata', {}).get('annotations', {}))
                raw_data['spec']['template']['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('metadata', {}).get('labels', {}))
                raw_data['spec']['template']['spec']['node_selector'] = self.convert_labels_format(
                    raw_readonly.get('spec', {}).get('template', {}).get('spec', {}).get('node_selector', {}))
                raw_data['uid'] = raw_readonly.get('metadata', {}).get('uid', '')
                raw_data['ready'] = self._get_ready(raw_readonly.get('status', {}))
                raw_data['age'] = self.get_age(raw_readonly.get('metadata', {}).get('creation_timestamp', ''))
                raw_data['pods'] = self._get_pods(list_all_pod, list_all_replicaset,
                                                  raw_readonly.get('metadata', {}).get('uid', ''))

                labels = raw_data['metadata']['labels']

                deployment_data = Deployment(raw_data, strict=False)
                # _LOGGER.debug(f'deployment_data => {deployment_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                pod_resource = DeploymentResource({
                    'name': deployment_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': deployment_data,
                    'reference': deployment_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(DeploymentResponse({'resource': pod_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'WorkLoad', 'Deployment', pod_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

    @staticmethod
    def _get_ready(status):
        if status is None:
            status = {}

        ready = str(status.get('ready_replicas', 0)) + '/' + str(status.get('replicas', 0))
        return ready

    def _get_pods(self, list_pods, list_replicasets, deployment_uid):
        # owner reference of replicaset and deployment uid need to be matched
        # owner reference of pod and replicaset uid need to be matched
        # pod -> replicaset -> deployment
        pods_for_deployment = []
        for pod in list_pods:
            raw_pod = pod.to_dict()
            pod_owner_reference = raw_pod.get('metadata', {}).get('owner_references', [])[0]
            for replicaset in list_replicasets:
                raw_replicaset = replicaset.to_dict()
                replicaset_owner_reference = raw_replicaset.get('metadata', {}).get('owner_references', [])[0]
                if deployment_uid == replicaset_owner_reference.get('uid', '') and \
                        raw_replicaset.get('metadata', {}).get('uid', '') == pod_owner_reference.get('uid', ''):
                    matched_pod = self._convert_pod_data(pod)
                    pods_for_deployment.append(matched_pod)
        return pods_for_deployment



