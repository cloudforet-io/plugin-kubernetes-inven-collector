from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.config.custom_resource_definition.data import CustomResourceDefinition
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
CUSTOM RESOURCE DEFINITION
'''

metadata = ItemDynamicLayout.set_fields('Metadata', root_path='data.metadata', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Uid', 'uid'),
    TextDyField.data_source('Generation', 'generation'),
    DateTimeDyField.data_source('Creation Timestamp', 'creation_timestamp')
])

crd_spec_base = ItemDynamicLayout.set_fields('Spec', root_path='data.spec', fields=[
    TextDyField.data_source('Conversion', 'conversion'),
    TextDyField.data_source('Group', 'group'),
    TextDyField.data_source('Names', 'names'),
    TextDyField.data_source('Scope', 'scope')
])

crd_spec_names_base = SimpleTableDynamicLayout.set_fields('Names', root_path='data.spec.names', fields=[
    TextDyField.data_source('Name', 'key'),
    TextDyField.data_source('Value', 'value')
])

crd_spec = ListDynamicLayout.set_layouts('Spec', layouts=[
    crd_spec_base,
    crd_spec_names_base])

versions = TableDynamicLayout.set_fields('Versions', root_path='data.spec.versions', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Served', 'served'),
    TextDyField.data_source('Storage', 'storage')
])

conditions = TableDynamicLayout.set_fields('Conditions', root_path='data.status.conditions', fields=[
    TextDyField.data_source('Type', 'type'),
    TextDyField.data_source('Status', 'status'),
    TextDyField.data_source('Message', 'message'),
    TextDyField.data_source('Reason', 'reason')
])

annotations = TableDynamicLayout.set_fields('Annotations', root_path='data.metadata.annotations', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

additional_printer_columns = TableDynamicLayout.set_fields('Additional Printer Columns', root_path='spec.additional_printer_columns', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Type', 'type'),
    TextDyField.data_source('Json Path', 'json_path')
])

crd_meta = CloudServiceMeta.set_layouts([metadata, crd_spec, versions, conditions, additional_printer_columns, annotations, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Config')


class CustomResourceDefinitionResource(ServiceResource):
    cloud_service_type = StringType(default='CustomResourceDefinition')
    data = ModelType(CustomResourceDefinition)
    _metadata = ModelType(CloudServiceMeta, default=crd_meta, serialized_name='metadata')


class CustomResourceDefinitionResourceResponse(CloudServiceResponse):
    resource = PolyModelType(CustomResourceDefinitionResource)
