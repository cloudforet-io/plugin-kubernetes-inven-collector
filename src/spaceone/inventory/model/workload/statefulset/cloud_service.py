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

stateful_set_pods = TableDynamicLayout.set_fields('Pods', root_path='data.pods', fields=[
    TextDyField.data_source('Name', 'metadata.name'),
    EnumDyField.data_source('Status', 'status.phase', default_state={
        'safe': ['Running', 'Succeeded'],
        'alert': ['Pending', 'Failed', 'Unknown']
    }),
    TextDyField.data_source('Containers', 'containers'),
    TextDyField.data_source('Namespace', 'metadata.namespace'),
    TextDyField.data_source('Node Name', 'spec.node_name'),
    TextDyField.data_source('Age', 'age')
])

annotations = TableDynamicLayout.set_fields('Annotations', root_path='data.metadata.annotations', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

stateful_set_meta = CloudServiceMeta.set_layouts([stateful_set_pods, annotations, labels])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default='WorkLoad')


class StatefulSetResource(WorkLoadResource):
    cloud_service_type = StringType(default='StatefulSet')
    data = ModelType(StatefulSet)
    _metadata = ModelType(CloudServiceMeta, default=stateful_set_meta, serialized_name='metadata')


class StatefulSetResponse(CloudServiceResponse):
    resource = PolyModelType(StatefulSetResource)
