from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.workload.statefulset.data import StatefulSet
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
StatefulSet
'''

stateful_set_meta = CloudServiceMeta.set_layouts([])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default='WorkLoad')


class StatefulSetResource(WorkLoadResource):
    cloud_service_type = StringType(default='StatefulSet')
    data = ModelType(StatefulSet)
    _metadata = ModelType(CloudServiceMeta, default=stateful_set_meta, serialized_name='metadata')


class StatefulSetResponse(CloudServiceResponse):
    resource = PolyModelType(StatefulSetResource)
