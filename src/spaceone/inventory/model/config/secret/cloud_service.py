from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.config.secret.data import Secret
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
)
from spaceone.inventory.libs.schema.cloud_service import (
    CloudServiceResource,
    CloudServiceResponse,
    CloudServiceMeta,
)

"""
Secret
"""

secret_base = ItemDynamicLayout.set_fields(
    "Base",
    fields=[
        DateTimeDyField.data_source(
            "Creation Timestamp", "data.metadata.creation_timestamp"
        ),
        TextDyField.data_source("Type", "data.type"),
        TextDyField.data_source("Name", "data.metadata.name"),
        TextDyField.data_source("Namespace", "data.metadata.namespace"),
        TextDyField.data_source("Uid", "data.uid"),
    ],
)

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

secret_meta = CloudServiceMeta.set_layouts([secret_base, data, annotations, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="Config")


class SecretResource(ServiceResource):
    cloud_service_type = StringType(default="Secret")
    data = ModelType(Secret)
    _metadata = ModelType(
        CloudServiceMeta, default=secret_meta, serialized_name="metadata"
    )


class SecretResponse(CloudServiceResponse):
    resource = PolyModelType(SecretResource)
