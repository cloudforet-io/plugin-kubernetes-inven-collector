import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['ServiceAccountConnector']
_LOGGER = logging.getLogger(__name__)


class ServiceAccountConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_service_account(self, **query) -> list:
        response = self.core_v1_client.list_service_account_for_all_namespaces(watch=False)
        return response.items

    # Check kubernetes version to get ingress client
    def _check_kubernetes_version(self):
        """
        Ingress api client is different from kubernetes version
        :return:
        """
        version = ''
        return version