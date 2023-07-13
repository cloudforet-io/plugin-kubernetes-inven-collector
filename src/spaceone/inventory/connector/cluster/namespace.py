import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ["NamespaceConnector"]
_LOGGER = logging.getLogger(__name__)


class NamespaceConnector(KubernetesConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_namespace(self, **query) -> list:
        response = self.core_v1_client.list_namespace(watch=False)
        return response.items
