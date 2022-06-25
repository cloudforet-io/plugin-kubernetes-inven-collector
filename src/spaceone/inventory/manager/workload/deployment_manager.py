import logging

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

        for deployment in list_all_deployment:
            try:
                #_LOGGER.debug(f'deployment => {deployment.to_dict()}')
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
                raw_data['metadata']['labels'] = self.convert_labels_format(raw_data.get('metadata', {}).get('labels', {}))

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
                raw_data['uid'] = raw_readonly['metadata']['uid']

                labels = raw_data['metadata']['labels']

                deployment_data = Deployment(raw_data, strict=False)
                #_LOGGER.debug(f'deployment_data => {deployment_data.to_primitive()}')

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

