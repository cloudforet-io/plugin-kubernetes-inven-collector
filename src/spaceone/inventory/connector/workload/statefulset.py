import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['StatefulSetConnector']
_LOGGER = logging.getLogger(__name__)


class StatefulSetConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_stateful_set(self, **query) -> list:
        response = self.apps_v1_client.list_stateful_set_for_all_namespaces()
        return response.items
