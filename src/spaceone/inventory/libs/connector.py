import os
import logging

from kubernetes import client
from spaceone.core.connector import BaseConnector
from kubernetes.config.kube_config import KubeConfigLoader

DEFAULT_SCHEMA = 'google_oauth_client_id'
_LOGGER = logging.getLogger(__name__)


class KubernetesConnector(BaseConnector):
    cert_filename = ''

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
        _LOGGER.debug(f'start k8s connector')
        super().__init__(transaction=None, config=None)
        secret_data = kwargs.get('secret_data')
        # Configure API Client

        loader = KubeConfigLoader(
            config_dict=secret_data
        )

        configuration = client.Configuration()
        loader.load_and_set(configuration)
        config = client.ApiClient(configuration)
        self.client = client.CoreV1Api(config)

    def verify(self, **kwargs):
        if self.client is None:
            self.set_connect(**kwargs)
