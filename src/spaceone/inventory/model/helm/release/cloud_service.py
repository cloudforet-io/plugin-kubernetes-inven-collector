from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.helm.release.data import Release
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Release(Helm)
'''

release_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Helm')


class ReleaseResource(ServiceResource):
    cloud_service_type = StringType(default='Release')
    data = ModelType(Release)
    _metadata = ModelType(CloudServiceMeta, default=release_meta, serialized_name='metadata')


class ReleaseResponse(CloudServiceResponse):
    resource = PolyModelType(ReleaseResource)
