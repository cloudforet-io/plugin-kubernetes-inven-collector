import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['ApplicationConnector']
_LOGGER = logging.getLogger(__name__)


class ReleaseConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_helm_labeled_secret(self, **query) -> list:
        response = self.core_v1_client.list_secret_for_all_namespaces(label_selector="owner=helm")
        return response.items

    # Check kubernetes version to get ingress client
    def _check_kubernetes_version(self):
        """
        Ingress api client is different from kubernetes version
        :return:
        """
        version = ''
        return version