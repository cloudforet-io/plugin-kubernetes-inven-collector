from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cluster.namespace.data import Namespace
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Namespace
'''

namespace_meta = CloudServiceMeta.set_layouts([])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default='Cluster')


class NamespaceResource(WorkLoadResource):
    cloud_service_type = StringType(default='Namespace')
    data = ModelType(Namespace)
    _metadata = ModelType(CloudServiceMeta, default=namespace_meta, serialized_name='metadata')


class NamespaceResponse(CloudServiceResponse):
    resource = PolyModelType(NamespaceResource)
