from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cluster.node.data import Node
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Node
'''

node_meta = CloudServiceMeta.set_layouts([])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default='Cluster')


class NodeResource(WorkLoadResource):
    cloud_service_type = StringType(default='Node')
    data = ModelType(Node)
    _metadata = ModelType(CloudServiceMeta, default=node_meta, serialized_name='metadata')


class NodeResponse(CloudServiceResponse):
    resource = PolyModelType(NodeResource)
