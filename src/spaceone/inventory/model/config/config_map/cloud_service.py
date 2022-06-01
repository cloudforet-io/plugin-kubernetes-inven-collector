from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.config.config_map.data import ConfigMap
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Config Map
'''

config_map_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Config')


class ConfigMapResource(ServiceResource):
    cloud_service_type = StringType(default='ConfigMap')
    data = ModelType(ConfigMap)
    _metadata = ModelType(CloudServiceMeta, default=config_map_meta, serialized_name='metadata')


class ConfigMapResponse(CloudServiceResponse):
    resource = PolyModelType(ConfigMapResource)