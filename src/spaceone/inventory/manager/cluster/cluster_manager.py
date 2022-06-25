import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.cluster.cluster import ClusterConnector
from spaceone.inventory.model.cluster.cluster.cloud_service import ClusterResource, ClusterResponse
from spaceone.inventory.model.cluster.cluster.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.cluster.cluster.data import Cluster

_LOGGER = logging.getLogger(__name__)


class ClusterManager(KubernetesManager):
    connector_name = 'ClusterConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Cluster Start **')
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
        cluster_name = self.get_cluster_name(secret_data)
        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        cluster_conn: ClusterConnector = self.locator.get_connector(self.connector_name, **params)
        cluster = self._get_cluster_data(cluster_name, cluster_conn)

        try:
            ##################################
            # 1. Set Basic Information
            ##################################
            region = 'global'

            _LOGGER.debug(f'cluster => {cluster}')
            ##################################
            # 2. Make Base Data
            ##################################
            # key:value type data need to be processed separately
            # Convert object to dict
            raw_data = cluster

            cluster_data = Cluster(raw_data, strict=False)
            _LOGGER.debug(f'cluster_data => {cluster_data.to_primitive()}')

            ##################################
            # 3. Make Return Resource
            ##################################
            cluster_resource = ClusterResource({
                'name': cluster_name,
                'account': cluster_name,
                'region_code': region,
                'data': cluster_data,
                'reference': cluster_data.reference()
            })

            ##################################
            # 4. Make Collected Region Code
            ##################################
            self.set_region_code(region)

            ##################################
            # 5. Make Resource Response Object
            # List of InstanceResponse Object
            ##################################
            collected_cloud_services.append(ClusterResponse({'resource': cluster_resource}))

        except Exception as e:
            _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
            # Pod name is key
            error_response = self.generate_resource_error_response(e, 'Cluster', 'Cluster', cluster_name)
            error_responses.append(error_response)

        return collected_cloud_services, error_responses

    def _get_cluster_data(self, cluster_name, cluster_conn):
        list_node = cluster_conn.list_node()
        list_pod = cluster_conn.list_pod()
        #_LOGGER.debug(f'list_node => {list_node}')


        return {
            "uid": cluster_name,
            "name": cluster_name,
            "state": self._get_cluster_state(list_node),
            "kubernetes_provider": self.get_kubernetes_provider(list_node),
            "version": self.get_kubernetes_version(list_node),
            "cpu_total": self._get_cpu_total(list_node),
            "cpu_assigned": self._get_cpu_current(list_node, list_pod),
            "memory_total": self._get_memory_total(list_node),
            "memory_assigned": self._get_memory_current(list_node, list_pod),
            "pod_total": self._get_pod_count_total(list_node),
            "pod_assigned": self._get_pod_count_current(list_node, list_pod),
            "node_conditions": self._get_node_conditions(list_node)
        }

    @staticmethod
    def _get_cluster_state(list_node):
        cluster_node_ready_status = []
        for node in list_node:
            raw_node = node.to_dict()
            node_conditions = raw_node.get('status', {}).get('conditions', [])
            for node_condition in node_conditions:
                if node_condition.get('type', '') == "Ready":
                    cluster_node_ready_status.append(node_condition.get('status', "False"))

        _LOGGER.debug(f'cluster_node_ready_status => {cluster_node_ready_status}')
        if "False" in cluster_node_ready_status:
            return "NotReady"
        else:
            return "Ready"

    @staticmethod
    def _get_node_conditions(list_node) -> list:
        cluster_node_conditions = []
        for node in list_node:
            raw_node = node.to_dict()
            node_conditions = raw_node.get('status', {}).get('conditions', [])
            for node_condition in node_conditions:
                node_condition['name'] = raw_node.get('metadata', {}).get('name', '')
                cluster_node_conditions.append(node_condition)

        return cluster_node_conditions

    def _get_cpu_total(self, list_node):
        cpu_total = 0
        for node in list_node:
            cpu = self.get_cpu_total_per_node(node)
            # "cpu": "940m"
            cpu_total = cpu_total + int(cpu.replace('m', ''))

        return cpu_total/1000

    def _get_memory_total(self, list_node):
        memory_total_kilo = 0
        for node in list_node:
            memory = self.get_memory_total_per_node(node)
            # "memory": "1003292Ki"
            memory_total_kilo = memory_total_kilo + int(memory.replace('Ki', ''))

        return memory_total_kilo

    def _get_pod_count_total(self, list_node):
        pod_count_total = 0
        for node in list_node:
            pod_count = self.get_pod_count_total_per_node(node)
            # "pods": "110"
            pod_count_total = pod_count_total + pod_count

        return pod_count_total

    def _get_cpu_current(self, list_node, list_pod):
        cpu_current = 0

        return cpu_current/1000

    def _get_memory_current(self, list_node, list_pod):
        memory_current = 0

        return memory_current

    def _get_pod_count_current(self, list_node, list_pod):
        pod_count_current = 0

        return pod_count_current