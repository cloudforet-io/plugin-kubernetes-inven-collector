import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ["DeploymentConnector"]
_LOGGER = logging.getLogger(__name__)


class DeploymentConnector(KubernetesConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_deployment(self, **query) -> list:
        response = self.apps_v1_client.list_deployment_for_all_namespaces(watch=False)
        return response.items

    def list_pod(self, **query) -> list:
        response = self.core_v1_client.list_pod_for_all_namespaces(watch=False)
        return response.items

    def list_replicaset(self, **query) -> list:
        response = self.apps_v1_client.list_replica_set_for_all_namespaces(watch=False)
        return response.items
