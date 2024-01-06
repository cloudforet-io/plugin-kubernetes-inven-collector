from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.authorization.role.data import Role
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
Role
"""

role = ItemDynamicLayout.set_fields(
    "Role",
    fields=[
        TextDyField.data_source("Namespace", "data.metadata.namespace"),
        DateTimeDyField.data_source(
            "Creation Timestamp", "data.metadata.creation_timestamp"
        ),
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

rules = TableDynamicLayout.set_fields(
    "Rules",
    root_path="data.rules",
    fields=[
        ListDyField.data_source("API Groups", "api_groups"),
        ListDyField.data_source("Resources", "resources"),
        ListDyField.data_source("Verbs", "verbs"),
    ],
)


role_meta = CloudServiceMeta.set_layouts([role, annotations, labels, rules])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="Authorization")


class RoleResource(ServiceResource):
    cloud_service_type = StringType(default="Role")
    data = ModelType(Role)
    _metadata = ModelType(
        CloudServiceMeta, default=role_meta, serialized_name="metadata"
    )


class RoleResponse(CloudServiceResponse):
    resource = PolyModelType(RoleResource)
