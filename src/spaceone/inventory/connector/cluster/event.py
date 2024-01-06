import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ["EventConnector"]
_LOGGER = logging.getLogger(__name__)


class EventConnector(KubernetesConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_node(self, **query) -> list:
        response = self.event_v1_client.list_event_for_all_namespaces(watch=False)
        return response.items
