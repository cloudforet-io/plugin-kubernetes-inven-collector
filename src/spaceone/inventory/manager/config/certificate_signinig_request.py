import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.config.certificate_signing_request import CertificateSigningRequestConnector
from spaceone.inventory.model.config.certificate_signing_request.cloud_service import CertificateSigningRequestResource,\
    CertificateSigningRequestResponse
from spaceone.inventory.model.config.certificate_signing_request.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.config.certificate_signing_request.data import CertificateSigningRequest

_LOGGER = logging.getLogger(__name__)


class CertificateSigningRequestManager(KubernetesManager):
    connector_name = 'CertificateSigningRequestConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Certificate Signing Request Start **')
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
        secret_name = ''

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        csr_conn: CertificateSigningRequestConnector = self.locator.get_connector(self.connector_name, **params)
        list_all_csr = csr_conn.list_csr()
        #_LOGGER.debug(f'list_all_csr => {list_all_csr}')

        for csr in list_all_csr:
            try:
                #_LOGGER.debug(f'csr => {csr.to_dict()}')
                ##################################
                # 1. Set Basic Information
                ##################################
                csr_name = csr.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = 'global'

                #_LOGGER.debug(f'csr => {csr}')
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = csr.to_dict()
                raw_readonly = csr.to_dict()
                raw_data['metadata']['annotations'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('annotations', {}))
                raw_data['metadata']['labels'] = self.convert_labels_format(
                    raw_readonly.get('metadata', {}).get('labels', {}))
                raw_data['uid'] = raw_readonly['spec']['uid']

                labels = raw_data['metadata']['labels']

                csr_data = CertificateSigningRequest(raw_data, strict=False)
                _LOGGER.debug(f'csr_data => {csr_data.to_primitive()}')

                ##################################
                # 3. Make Return Resource
                ##################################
                csr_resource = CertificateSigningRequestResource({
                    'name': csr_name,
                    'account': cluster_name,
                    'tags': labels,
                    'region_code': region,
                    'data': csr_data,
                    'reference': csr_data.reference()
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(CertificateSigningRequestResponse({'resource': csr_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(e, 'Config', 'CertificateSigningRequest', csr_name)
                error_responses.append(error_response)

        return collected_cloud_services, error_responses

