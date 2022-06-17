import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['ClusterConnector']
_LOGGER = logging.getLogger(__name__)


class ClusterConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_node(self, **query) -> list:
        response = self.core_v1_client.list_node()
        return response.items

    def list_pod(self, **query) -> list:
        response = self.core_v1_client.list_pod_for_all_namespaces()
        return response.items



