import logging
import base64
import gzip
import json

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.application.application import ApplicationConnector
from spaceone.inventory.model.application.application.cloud_service import ApplicationResource, ApplicationResponse
from spaceone.inventory.model.application.application.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.application.application.data import Application

_LOGGER = logging.getLogger(__name__)


class ApplicationManager(KubernetesManager):
    connector_name = 'ApplicationConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Application Start **')
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
        application_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        application_conn: ApplicationConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_application = application_conn.list_secret()
        #_LOGGER.debug(f'list_all_application => {list_all_application}')

        for application in list_all_application:
            try:
                #_LOGGER.debug(f'application => {application.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                application_name = application.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'application => {application}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                encoded_data = application.to_dict()
                raw_data = self._base64_to_dict(encoded_data)
                _LOGGER.debug(f'raw_data => {raw_data}')
                application_data = Application(raw_data, strict=False)
                _LOGGER.debug(f'application_data => {application_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                application_resource = ApplicationResource({
                    'name': application_name,
                    'account': cluster_name,
                    'region_code': region,
                    'data': application_data,
                    'reference': application_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(ApplicationResponse({'resource': application_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Application', 'Application', application_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

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
        _LOGGER.debug(f'keys => {helm_data.keys()}')
        _LOGGER.debug(f'_base64_to_dict => {helm_data}')

        return helm_data


