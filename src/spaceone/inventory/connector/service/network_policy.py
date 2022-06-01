import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['NetworkPolicyConnector']
_LOGGER = logging.getLogger(__name__)


class NetworkPolicyConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_network_policy(self, **query) -> list:
        response = self.networking_v1_client.list_network_policy_for_all_namespaces()
        return response.items

    # Check kubernetes version to get ingress client
    def _check_kubernetes_version(self):
        """
        Ingress api client is different from kubernetes version
        :return:
        """
        version = ''
        return version