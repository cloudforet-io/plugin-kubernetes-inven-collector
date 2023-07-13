from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.service.ingress.data import Ingress
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
Ingress
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

ingress_meta = CloudServiceMeta.set_layouts([annotations, labels])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="Service")


class IngressResource(ServiceResource):
    cloud_service_type = StringType(default="Ingress")
    data = ModelType(Ingress)
    _metadata = ModelType(
        CloudServiceMeta, default=ingress_meta, serialized_name="metadata"
    )


class IngressResponse(CloudServiceResponse):
    resource = PolyModelType(IngressResource)
