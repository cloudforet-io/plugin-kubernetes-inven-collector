from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.authentication.service_account.data import ServiceAccount
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Service Account
'''

service_account_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Authentication')


class ServiceAccountResource(ServiceResource):
    cloud_service_type = StringType(default='ServiceAccount')
    data = ModelType(ServiceAccount)
    _metadata = ModelType(CloudServiceMeta, default=service_account_meta, serialized_name='metadata')


class ServiceAccountResponse(CloudServiceResponse):
    resource = PolyModelType(ServiceAccountResource)
