import logging

from spaceone.inventory.libs.connector import KubernetesConnector

__all_ = ['CertificateSigningRequestConnector']
_LOGGER = logging.getLogger(__name__)


class CertificateSigningRequestConnector(KubernetesConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_csr(self, **query) -> list:
        response = self.certificate_v1_client.list_certificate_signing_request()
        return response.items

    # Check kubernetes version to get ingress client
    def _check_kubernetes_version(self):
        """
        Ingress api client is different from kubernetes version
        :return:
        """
        version = ''
        return version