from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.authorization.cluster_role.data import ClusterRole
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
Cluster Role
"""

cluster_role = ItemDynamicLayout.set_fields(
    "Cluster Role",
    fields=[
        DateTimeDyField.data_source(
            "Creation Timestamp", "data.metadata.creation_timestamp"
        ),
        TextDyField.data_source("Uid", "data.metadata.uid"),
        TextDyField.data_source("Aggregation Rule", "data.aggregation_rule"),
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

rules = TableDynamicLayout.set_fields(
    "Rules",
    root_path="data.rules",
    fields=[
        ListDyField.data_source("API Groups", "api_groups"),
        ListDyField.data_source("Resources", "resources"),
        ListDyField.data_source("Verbs", "verbs"),
    ],
)

cluster_role_meta = CloudServiceMeta.set_layouts(
    [cluster_role, annotations, labels, rules]
)


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="Authorization")


class ClusterRoleResource(ServiceResource):
    cloud_service_type = StringType(default="ClusterRole")
    data = ModelType(ClusterRole)
    _metadata = ModelType(
        CloudServiceMeta, default=cluster_role_meta, serialized_name="metadata"
    )


class ClusterRoleResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterRoleResource)
