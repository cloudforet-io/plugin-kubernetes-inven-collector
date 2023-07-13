from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.config.config_map.data import ConfigMap
from spaceone.inventory.libs.schema.metadata.dynamic_field import (
    TextDyField,
    DateTimeDyField,
    EnumDyField,
    ListDyField,
    DictDyField,
)
from spaceone.inventory.libs.schema.metadata.dynamic_layout import (
    ItemDynamicLayout,
    TableDynamicLayout,
    ListDynamicLayout,
    SimpleTableDynamicLayout,
    RawDynamicLayout,
)
from spaceone.inventory.libs.schema.cloud_service import (
    CloudServiceResource,
    CloudServiceResponse,
    CloudServiceMeta,
)

"""
Config Map
"""


data = TableDynamicLayout.set_fields(
    "Data",
    root_path="data.data",
    fields=[
        TextDyField.data_source("Config", "key"),
        TextDyField.data_source("Value", "value"),
    ],
)

annotations = TableDynamicLayout.set_fields(
    "Annotations",
    root_path="data.metadata.annotations",
    fields=[
        TextDyField.data_source("Key", "key"),
        TextDyField.data_source("Value", "value"),
    ],
)

labels = TableDynamicLayout.set_fields(
    "Labels",
    root_path="data.metadata.labels",
    fields=[
        TextDyField.data_source("Key", "key"),
        TextDyField.data_source("Value", "value"),
    ],
)


config_map_meta = CloudServiceMeta.set_layouts([data, annotations, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="Config")


class ConfigMapResource(ServiceResource):
    cloud_service_type = StringType(default="ConfigMap")
    data = ModelType(ConfigMap)
    _metadata = ModelType(
        CloudServiceMeta, default=config_map_meta, serialized_name="metadata"
    )


class ConfigMapResponse(CloudServiceResponse):
    resource = PolyModelType(ConfigMapResource)
