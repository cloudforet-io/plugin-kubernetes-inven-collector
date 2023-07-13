from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cluster.node.data import Node
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
Node
"""

node_base = ItemDynamicLayout.set_fields(
    "Base",
    fields=[
        TextDyField.data_source("Name", "name"),
        EnumDyField.data_source(
            "Status",
            "data.display.status",
            default_badge={"green.500": ["Ready"], "red.500": ["NotReady"]},
        ),
        TextDyField.data_source("Uid", "data.metadata.uid"),
        DateTimeDyField.data_source("Created", "data.metadata.creation_timestamp"),
    ],
)

node_allocatable = ItemDynamicLayout.set_fields(
    "Allocatable",
    root_path="data.status.allocatable",
    fields=[
        TextDyField.data_source("CPU", "cpu"),
        TextDyField.data_source("Ephemeral-Storage", "ephemeral-storage"),
        TextDyField.data_source("Hugepages-1Gi", "hugepages-1Gi"),
        TextDyField.data_source("Hugepages-2Mi", "hugepages-2Mi"),
        TextDyField.data_source("Memory", "memory"),
        TextDyField.data_source("Pods", "pods"),
    ],
)

node_capacity = ItemDynamicLayout.set_fields(
    "Capacity",
    root_path="data.status.capacity",
    fields=[
        TextDyField.data_source("CPU", "cpu"),
        TextDyField.data_source("Ephemeral-storage", "ephemeral-storage"),
        TextDyField.data_source("Hugepages-1Gi", "hugepages-1Gi"),
        TextDyField.data_source("Hugepages-2Mi", "hugepages-2Mi"),
        TextDyField.data_source("Memory", "memory"),
        TextDyField.data_source("Pods", "pods"),
    ],
)

node_layout = ListDynamicLayout.set_layouts(
    "Node", layouts=[node_base, node_allocatable, node_capacity]
)

annotations = TableDynamicLayout.set_fields(
    "Annotation",
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

address = TableDynamicLayout.set_fields(
    "Address",
    root_path="data.status.addresses",
    fields=[
        TextDyField.data_source("Type", "type"),
        TextDyField.data_source("Address", "address"),
    ],
)

condition = TableDynamicLayout.set_fields(
    "Condition",
    root_path="data.status.conditions",
    fields=[
        TextDyField.data_source("Type", "type"),
        EnumDyField.data_source(
            "Status",
            "state",
            default_badge={"green.500": ["true"], "red.500": ["false"]},
        ),
        TextDyField.data_source("Message", "message"),
        TextDyField.data_source("Reason", "reason"),
    ],
)

images = TableDynamicLayout.set_fields(
    "Images",
    root_path="data.status.images",
    fields=[
        ListDyField.data_source("Names", "names"),
        TextDyField.data_source("Size Bytes", "size_bytes"),
    ],
)

node_meta = CloudServiceMeta.set_layouts(
    [node_layout, annotations, labels, address, condition, images]
)


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default="Cluster")


class NodeResource(WorkLoadResource):
    cloud_service_type = StringType(default="Node")
    data = ModelType(Node)
    _metadata = ModelType(
        CloudServiceMeta, default=node_meta, serialized_name="metadata"
    )


class NodeResponse(CloudServiceResponse):
    resource = PolyModelType(NodeResource)
