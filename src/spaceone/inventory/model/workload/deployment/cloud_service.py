from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.workload.deployment.data import Deployment
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Deployment
'''

annotations = TableDynamicLayout.set_fields('Annotations', root_path='data.metadata.annotations', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

deployment_meta = CloudServiceMeta.set_layouts([annotations, labels])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default='WorkLoad')


class DeploymentResource(WorkLoadResource):
    cloud_service_type = StringType(default='Deployment')
    data = ModelType(Deployment)
    _metadata = ModelType(CloudServiceMeta, default=deployment_meta, serialized_name='metadata')


class DeploymentResponse(CloudServiceResponse):
    resource = PolyModelType(DeploymentResource)
