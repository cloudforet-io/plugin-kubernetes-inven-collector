from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cluster.namespace.data import Namespace
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
Namespace
"""

namespace = ItemDynamicLayout.set_fields(
    "Details",
    fields=[
        TextDyField.data_source("Name", "name"),
        TextDyField.data_source("Status", "data.status.phase"),
        DateTimeDyField.data_source("Created", "data.metadata.creation_timestamp"),
        TextDyField.data_source("Uid", "data.metadata.uid"),
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

namespace_meta = CloudServiceMeta.set_layouts([namespace, annotations, labels])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default="Cluster")


class NamespaceResource(WorkLoadResource):
    cloud_service_type = StringType(default="Namespace")
    data = ModelType(Namespace)
    _metadata = ModelType(
        CloudServiceMeta, default=namespace_meta, serialized_name="metadata"
    )


class NamespaceResponse(CloudServiceResponse):
    resource = PolyModelType(NamespaceResource)
