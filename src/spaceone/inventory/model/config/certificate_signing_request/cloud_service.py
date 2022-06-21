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
certificate_signing_request = ItemDynamicLayout.set_fields('CSR', root_path='data.metadata', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Uid', 'uid'),
    DateTimeDyField.data_source('Creation Timestamp', 'creation_timestamp')
])

spec = ItemDynamicLayout.set_fields('Spec', root_path='data.spec', fields=[
    TextDyField.data_source('Uid', 'uid'),
    TextDyField.data_source('Signer Name', 'signer_name'),
    TextDyField.data_source('User Name', 'username'),
    ListDyField.data_source('Usages', 'usages'),
    TextDyField.data_source('Expiration Seconds', 'expiration_seconds'),
    ListDyField.data_source('Groups', 'groups')
])

annotations = TableDynamicLayout.set_fields('Annotations', root_path='data.metadata.annotations', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

certificate_signing_request_meta = CloudServiceMeta.set_layouts([certificate_signing_request, spec, annotations, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Config')


class CertificateSigningRequestResource(ServiceResource):
    cloud_service_type = StringType(default='CertificateSigningRequest')
    data = ModelType(CertificateSigningRequest)
    _metadata = ModelType(CloudServiceMeta, default=certificate_signing_request_meta, serialized_name='metadata')


class CertificateSigningRequestResponse(CloudServiceResponse):
    resource = PolyModelType(CertificateSigningRequestResource)
