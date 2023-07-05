import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['CustomResourceDefinitionConnector']
_LOGGER = logging.getLogger(__name__)


class CustomResourceDefinitionConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_custom_resource_definition(self, **query) -> list:
        response = self.api_extensions_v1_client.list_custom_resource_definition(watch=False)
        return response.items

    # Check kubernetes version to get ingress client
    def _check_kubernetes_version(self):
        """
        Ingress api client is different from kubernetes version
        :return:
        """
        version = ''
        return version