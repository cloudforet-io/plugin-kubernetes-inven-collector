import logging
import base64
import gzip
import json
import time

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.helm.release import ReleaseConnector
from spaceone.inventory.model.helm.release.cloud_service import ReleaseResource, ReleaseResponse
from spaceone.inventory.model.helm.release.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.helm.release.data import Release

_LOGGER = logging.getLogger(__name__)


class ReleaseManager(KubernetesManager):
    connector_name = 'ReleaseConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Release Start **')
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        collected_cloud_services = []
        error_responses = []

        secret_data = params['secret_data']
        release_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        release_conn: ReleaseConnector = self.locator.get_connector(self.connector_name, **params)
        # Helm Labeled secrets are helm history for each release
        list_helm_labeled_secret = release_conn.list_helm_labeled_secret()
        #list_all_release = self._get_all_releases(list_helm_labeled_secret)

        #_LOGGER.debug(f'list_all_release => {list_helm_labeled_secret}')

        #for release in list_all_release:
        for release in list_helm_labeled_secret:
            try:
                #_LOGGER.debug(f'helm => {release.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                release_name = release.metadata.name
                uid = '-'.join([release.metadata.uid, release.metadata.namespace])
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'helm => {helm}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                encoded_data = release.to_dict()
                raw_data = self._base64_to_dict(encoded_data)
                raw_readonly = raw_data
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = uid

                labels = raw_data['metadata']['labels']
                _LOGGER.debug(f'raw_data => {raw_data}')
                release_data = Release(raw_data, strict=False)
                _LOGGER.debug(f'release_data => {release_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                release_resource = ReleaseResource({
                    'name': release_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': release_data,
                    'reference': release_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(ReleaseResponse({'resource': release_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Helm', 'Release', release_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses


    def _get_all_releases(self, list_all_secrets):
        all_releases = []
        all_name_and_namespaces = self._get_release_name_and_namespace(list_all_secrets)
        _LOGGER.debug(f'_get_all_releases => {all_name_and_namespaces}')

        for n in all_name_and_namespaces:
            latest_release = self._get_latest_release(n, list_all_secrets)
            all_releases.append(latest_release)

        return all_releases


    def _get_latest_release(self, name_and_namespaces, list_all_secrets):

        return


    def _get_release_name_and_namespace(self, list_all_secrets):
        list_release_name_and_namespace = []
        for secret in list_all_secrets:
            i = {
                'release_name': self._get_release_name(secret.metadata.name),
                'namespace': secret.metadata.namespace
            }
            # release_name and namespace pair can be duplicated
            if i not in list_release_name_and_namespace:
                list_release_name_and_namespace.append(i)

        return list_release_name_and_namespace

    @staticmethod
    def _get_release_name(helm_secret_full_name):
        if len(helm_secret_full_name) > 2:
            return helm_secret_full_name.split('.')[-2]
        else:
            return ''


    def _get_single_release_info(self, list_all_secrets):
        return {
            'release_name': '',
            'namespace': '',
            'revision': '',
            'updated_timestamp': '',
            'status': '',
            'chart': '',
            'app_version': ''
        }

    def _get_history(self, release_name, release_namespace, list_all_secrets):
        history = {
            'release_name': '',
            'namespace': '',
            'updated': '',
            'status': '',
            'chart': '',
            'app_version': '',
            'description': ''
        }
        list_history = []
        return list_history

    def _get_chart_info(self, release_name, release_namespace, list_all_secrets):
        matched_secrets = {}
        return matched_secrets.get('data', {}).get('release', {}).get('chart', {})

    @staticmethod
    def _base64_to_dict(helm_data):
        """
        Convert helm release data into json
        base64(secret) -> base64(helm) -> gzip -> (helm)
        :param helm_release_data: 
        :return: 
        """

        base64_base64_bytes = helm_data.get('data', {}).get('release', '').encode('ascii')
        base64_bytes = base64.decodebytes(base64_base64_bytes)
        gzip_bytes = base64.decodebytes(base64_bytes)
        message_bytes = gzip.decompress(gzip_bytes)
        helm_data['data']['release'] = json.loads(message_bytes.decode('utf-8'))
        #_LOGGER.debug(f'keys => {helm_data.keys()}')
        #_LOGGER.debug(f'_base64_to_dict => {helm_data}')

        return helm_data


