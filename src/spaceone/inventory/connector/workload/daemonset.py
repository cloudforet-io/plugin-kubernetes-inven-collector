import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['DaemonSetConnector']
_LOGGER = logging.getLogger(__name__)


class DaemonSetConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_daemon_set(self, **query) -> list:
        response = self.apps_v1_client.list_daemon_set_for_all_namespaces(watch=False)
        return response.items

    def list_pod(self, **query) -> list:
        response = self.core_v1_client.list_pod_for_all_namespaces(watch=False)
        return response.items
