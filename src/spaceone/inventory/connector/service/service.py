import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['ServiceConnector']
_LOGGER = logging.getLogger(__name__)


class ServiceConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_service(self, **query) -> list:
        response = self.core_v1_client.list_service_for_all_namespaces(watch=False)
        return response.items
