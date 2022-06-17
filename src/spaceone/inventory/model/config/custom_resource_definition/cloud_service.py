from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.config.custom_resource_definition.data import CustomResourceDefinition
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
CUSTOM RESOURCE DEFINITION
'''

crd_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Config')


class CustomResourceDefinitionResource(ServiceResource):
    cloud_service_type = StringType(default='CustomResourceDefinition')
    data = ModelType(CustomResourceDefinition)
    _metadata = ModelType(CloudServiceMeta, default=crd_meta, serialized_name='metadata')


class CustomResourceDefinitionResourceResponse(CloudServiceResponse):
    resource = PolyModelType(CustomResourceDefinitionResource)
