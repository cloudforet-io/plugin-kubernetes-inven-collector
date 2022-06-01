from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.authorization.cluster_role.data import ClusterRole
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Cluster Role
'''

cluster_role_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Authorization')


class ClusterRoleResource(ServiceResource):
    cloud_service_type = StringType(default='ClusterRole')
    data = ModelType(ClusterRole)
    _metadata = ModelType(CloudServiceMeta, default=cluster_role_meta, serialized_name='metadata')


class ClusterRoleResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterRoleResource)
