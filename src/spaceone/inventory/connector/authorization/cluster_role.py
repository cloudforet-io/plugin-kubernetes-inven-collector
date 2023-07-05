import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['ClusterRoleConnector']
_LOGGER = logging.getLogger(__name__)


class ClusterRoleConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_cluster_role(self, **query) -> list:
        response = self.rbac_authorization_v1_client.list_cluster_role(watch=False)
        return response.items

    # Check kubernetes version to get ingress client
    def _check_kubernetes_version(self):
        """
        Ingress api client is different from kubernetes version
        :return:
        """
        version = ''
        return version