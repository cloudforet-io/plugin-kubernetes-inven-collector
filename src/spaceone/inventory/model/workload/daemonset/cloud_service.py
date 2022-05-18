from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.workload.daemonset.data import DaemonSet
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
DaemonSet
'''

daemon_set_meta = CloudServiceMeta.set_layouts([])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default='WorkLoad')


class DaemonSetResource(WorkLoadResource):
    cloud_service_type = StringType(default='DaemonSet')
    data = ModelType(DaemonSet)
    _metadata = ModelType(CloudServiceMeta, default=daemon_set_meta, serialized_name='metadata')


class DaemonSetResponse(CloudServiceResponse):
    resource = PolyModelType(DaemonSetResource)
