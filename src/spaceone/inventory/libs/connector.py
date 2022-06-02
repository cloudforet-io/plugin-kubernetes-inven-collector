import os
import logging

from kubernetes import client
from spaceone.core.connector import BaseConnector
from kubernetes.config.kube_config import KubeConfigLoader

DEFAULT_SCHEMA = 'google_oauth_client_id'
_LOGGER = logging.getLogger(__name__)


class KubernetesConnector(BaseConnector):

    def __init__(self, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data

        secret_data(dict)
            - type: ..
            - project_id: ...
            - token_uri: ...
            - ...
        """
        super().__init__(transaction=None, config=None)
        secret_data = kwargs.get('secret_data')

        # Configure API Client
        kube_config = self._get_kube_config(secret_data)
        loader = KubeConfigLoader(
            config_dict=kube_config
        )

        configuration = client.Configuration()
        loader.load_and_set(configuration)
        self.config = client.ApiClient(configuration)
        self.core_v1_client = client.CoreV1Api(self.config)
        self.apps_v1_client = client.AppsV1Api(self.config)
        self.networking_v1_client = client.NetworkingV1Api(self.config)
        self.storage_v1_client = client.StorageV1Api(self.config)
        self.rbac_authorization_v1_client = client.RbacAuthorizationV1Api(self.config)
        self.certificate_v1_client = client.CertificatesV1Api(self.config)
        self.api_extensions_v1_client = client.ApiextensionsV1Api(self.config)

    def verify(self, **kwargs):
        if self.client is None:
            self.set_connect(**kwargs)

    @staticmethod
    def _get_kube_config(secret_data):
        """
        Returns kube-config style object from secret_data
        
        :param secret_data: 
        :return: kube_config  
        """
        return {
            "apiVersion": "v1",
            "clusters": [
                {
                    "cluster": {
                        "certificate-authority-data": secret_data.get('certificate_authority_data', ''),
                        "server": secret_data.get('server', '')
                    },
                    "name": secret_data.get('cluster_name', '')
                }
            ],
            "contexts": [
                {
                    "context": {
                        "cluster": secret_data.get('cluster_name', ''),
                        "user": secret_data.get('cluster_name', '')
                    },
                    "name": secret_data.get('cluster_name', '')
                }
            ],
            "current-context": secret_data.get('cluster_name', ''),
            "kind": "Config",
            "preferences": {},
            "users": [
                {
                    "name": secret_data.get('cluster_name', ''),
                    "user": {
                        "token": secret_data.get('token', '')
                    }
                }
            ]
        }
