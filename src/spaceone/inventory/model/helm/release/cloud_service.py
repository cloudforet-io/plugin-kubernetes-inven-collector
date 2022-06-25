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
release_base = ItemDynamicLayout.set_fields('Helm', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Namespace', 'data.metadata.namespace'),
    TextDyField.data_source('Creation Timestamp', 'data.metadata.creation_timestamp'),
    TextDyField.data_source('Uid', 'data.uid')
])

release_info = ItemDynamicLayout.set_fields('Release Info', fields=[
    TextDyField.data_source('Name', 'data.data.release.name'),
    TextDyField.data_source('Version', 'data.data.release.version'),
    TextDyField.data_source('First Deployed', 'data.data.release.info.first_deployed'),
    TextDyField.data_source('Last Deployed', 'data.data.release.info.last_deployed'),
    TextDyField.data_source('Deleted', 'data.data.release.info.deleted'),
    TextDyField.data_source('Description', 'data.data.release.info.description'),
    TextDyField.data_source('Status', 'data.data.release.info.status'),
    TextDyField.data_source('Manifest', 'data.data.release.manifest')
])

release_chart = ItemDynamicLayout.set_fields('Chart', root_path='data.data.release.chart', fields=[
    TextDyField.data_source('Name', 'metadata.name'),
    TextDyField.data_source('Home', 'metadata.home'),
    ListDyField.data_source('Sources', 'metadata.sources'),
    TextDyField.data_source('Version', 'metadata.version'),
    TextDyField.data_source('Description', 'metadata.description'),
    ListDyField.data_source('Keywords', 'metadata.keywords'),
    ListDyField.data_source('Maintainers', 'metadata.maintainers'),
    TextDyField.data_source('Icon', 'metadata.icon'),
    TextDyField.data_source('Api Version', 'metadata.api_version'),
    TextDyField.data_source('App Version', 'metadata.app_version')
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])


release_meta = CloudServiceMeta.set_layouts([release_base, release_info, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Helm')


class ReleaseResource(ServiceResource):
    cloud_service_type = StringType(default='Release')
    data = ModelType(Release)
    _metadata = ModelType(CloudServiceMeta, default=release_meta, serialized_name='metadata')


class ReleaseResponse(CloudServiceResponse):
    resource = PolyModelType(ReleaseResource)
