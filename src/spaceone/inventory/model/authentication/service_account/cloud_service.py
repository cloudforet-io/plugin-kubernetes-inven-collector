from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.authentication.service_account.data import ServiceAccount
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
Service Account
"""

service_account = ItemDynamicLayout.set_fields(
    "Service Account",
    fields=[
        TextDyField.data_source("Name", "name"),
        TextDyField.data_source("NameSpace", "data.metadata.namespace"),
        TextDyField.data_source("Uid", "data.metadata.uid"),
        DateTimeDyField.data_source(
            "Creation Timestamp", "data.metadata.creation_timestamp"
        ),
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

secret = SimpleTableDynamicLayout.set_fields(
    "Secret", root_path="data.secrets", fields=[TextDyField.data_source("Name", "name")]
)

service_account_meta = CloudServiceMeta.set_layouts(
    [service_account, annotations, labels, secret]
)


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="Authentication")


class ServiceAccountResource(ServiceResource):
    cloud_service_type = StringType(default="ServiceAccount")
    data = ModelType(ServiceAccount)
    _metadata = ModelType(
        CloudServiceMeta, default=service_account_meta, serialized_name="metadata"
    )


class ServiceAccountResponse(CloudServiceResponse):
    resource = PolyModelType(ServiceAccountResource)
