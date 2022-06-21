from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.config.certificate_signing_request.data import CertificateSigningRequest
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Certificate Signing Request
'''

annotations = TableDynamicLayout.set_fields('Annotations', root_path='data.metadata.annotations', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

certificate_signing_request_meta = CloudServiceMeta.set_layouts([annotations, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Config')


class CertificateSigningRequestResource(ServiceResource):
    cloud_service_type = StringType(default='CertificateSigningRequest')
    data = ModelType(CertificateSigningRequest)
    _metadata = ModelType(CloudServiceMeta, default=certificate_signing_request_meta, serialized_name='metadata')


class CertificateSigningRequestResponse(CloudServiceResponse):
    resource = PolyModelType(CertificateSigningRequestResource)
