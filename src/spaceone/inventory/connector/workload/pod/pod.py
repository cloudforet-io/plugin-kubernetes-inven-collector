import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['PodConnector']
_LOGGER = logging.getLogger(__name__)


class PodConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_pod(self, **query) -> list:
        response = self.client.list_pod_for_all_namespaces()
        #_LOGGER.debug(f'list_pod => {response.items}')
        return response.items
