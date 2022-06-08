from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.application.application.data import Application
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Application(Helm)
'''

application_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Application')


class ApplicationResource(ServiceResource):
    cloud_service_type = StringType(default='Application')
    data = ModelType(Application)
    _metadata = ModelType(CloudServiceMeta, default=application_meta, serialized_name='metadata')


class ApplicationResponse(CloudServiceResponse):
    resource = PolyModelType(ApplicationResource)
