import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.cluster.node import NodeConnector
from spaceone.inventory.model.cluster.node.cloud_service import NodeResponse, NodeResource
from spaceone.inventory.model.cluster.node.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.cluster.node.data import Node

_LOGGER = logging.getLogger(__name__)


class NodeManager(KubernetesManager):
    connector_name = 'NodeConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Node Start **')
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
        node_conn: NodeConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_node = node_conn.list_node()
        #_LOGGER.debug(f'list_all_deployment => {list_all_deployment}')

        for node in list_all_node:
            try:
                #_LOGGER.debug(f'deployment => {deployment.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                node_name = node.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'node => {node}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = node.to_dict()
                raw_readonly = node.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['metadata']['uid']

                node_data = Node(raw_data, strict=False)
                #_LOGGER.debug(f'node_data => {node_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                node_resource = NodeResource({
                    'name': node_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': node_data,
                    'reference': node_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(NodeResponse({'resource': node_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'WorkLoad', 'Node', pod_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

