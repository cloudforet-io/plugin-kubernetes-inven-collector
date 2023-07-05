import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['SecretConnector']
_LOGGER = logging.getLogger(__name__)


class SecretConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_secret(self, **query) -> list:
        response = self.core_v1_client.list_secret_for_all_namespaces(watch=False)
        return response.items

    # Check kubernetes version to get ingress client
    def _check_kubernetes_version(self):
        """
        Ingress api client is different from kubernetes version
        :return:
        """
        version = ''
        return version