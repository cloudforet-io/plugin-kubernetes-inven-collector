from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.authorization.role.data import Role
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Role
'''

role_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Authorization')


class RoleResource(ServiceResource):
    cloud_service_type = StringType(default='Role')
    data = ModelType(Role)
    _metadata = ModelType(CloudServiceMeta, default=role_meta, serialized_name='metadata')


class RoleResponse(CloudServiceResponse):
    resource = PolyModelType(RoleResource)
