import math
import json
import logging
import ipaddress
from urllib.parse import urlparse

from spaceone.core.manager import BaseManager
from spaceone.inventory.conf.cloud_service_conf import REGION_INFO
from spaceone.inventory.libs.connector import KubernetesConnector
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse


_LOGGER = logging.getLogger(__name__)


class KubernetesManager(BaseManager):
    connector_name = None
    cloud_service_types = []
    response_schema = None
    collected_region_codes = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: KubernetesConnector = KubernetesConnector(secret_data=secret_data)
        connector.verify()

    def collect_cloud_service_type(self, params):
        options = params.get('options', {})

        for cloud_service_type in self.cloud_service_types:
            if 'service_code_mappers' in options:
                svc_code_maps = options['service_code_mappers']
                if getattr(cloud_service_type.resource, 'service_code') and \
                        cloud_service_type.resource.service_code in svc_code_maps:
                    cloud_service_type.resource.service_code = svc_code_maps[cloud_service_type.resource.service_code]
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        total_resources = []

        try:
            # Collect Cloud Service Type3wee
            total_resources.extend(self.collect_cloud_service_type(params))

            # Collect Cloud Service
            resources, error_resources = self.collect_cloud_service(params)
            total_resources.extend(resources)
            total_resources.extend(error_resources)

            # Collect Region
            total_resources.extend(self.collect_region())

        except Exception as e:
            _LOGGER.error(f'[collect_resources] {e}', exc_info=True)
            error_resource_response = self.generate_error_response(e, self.cloud_service_types[0].resource.group, self.cloud_service_types[0].resource.name)
            total_resources.append(error_resource_response)

        return total_resources

    def collect_region(self):
        results = []
        for region_code in self.collected_region_codes:
            if region := self.match_region_info(region_code):
                results.append(RegionResponse({'resource': region}))

        return results

    def set_region_code(self, region):
        if region not in REGION_INFO:
            region = 'global'

        if region not in self.collected_region_codes:
            self.collected_region_codes.append(region)

    @staticmethod
    def convert_labels_format(labels):
        convert_labels = []
        if labels is not None:
            for k, v in labels.items():
                convert_labels.append({
                    'key': k,
                    'value': v
                })
        return convert_labels

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({
                'message': json.dumps(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})
        else:
            error_resource_response = ErrorResourceResponse({
                'message': str(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})

        return error_resource_response

    @staticmethod
    def generate_resource_error_response(e, cloud_service_group, cloud_service_type, resource_id):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({
                'message': json.dumps(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type,
                    'resource_id': resource_id
                }})
        else:
            error_resource_response = ErrorResourceResponse({
                'message': str(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type,
                    'resource_id': resource_id
                }})
        return error_resource_response

    @staticmethod
    def match_region_info(region_code):
        match_region_info = REGION_INFO.get(region_code)

        if match_region_info:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': region_code
            })
            return RegionResource(region_info, strict=False)

        return None

    @staticmethod
    def get_cluster_name(secret_data):
        """
        Get cluster name from secret_data(kubeconfig)
        :param secret_data:
        :return:
        """
        cluster_name = ''
        current_context = secret_data.get('current-context', '')
        list_contexts = secret_data.get('contexts', [])

        for context in list_contexts:
            if current_context == context.get('name', ''):
                cluster_name = context.get('context', {}).get('cluster', '')

        return cluster_name
