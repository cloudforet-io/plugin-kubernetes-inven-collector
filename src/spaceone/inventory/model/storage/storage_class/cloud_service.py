from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.storage.storage_class.data import StorageClass
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
Storage Class
"""

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

storage_class_meta = CloudServiceMeta.set_layouts([annotations, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="Storage")


class StorageClassResource(ServiceResource):
    cloud_service_type = StringType(default="StorageClass")
    data = ModelType(StorageClass)
    _metadata = ModelType(
        CloudServiceMeta, default=storage_class_meta, serialized_name="metadata"
    )


class StorageClassResponse(CloudServiceResponse):
    resource = PolyModelType(StorageClassResource)
