from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cluster.event.data import Event
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
Event
"""

event_meta = CloudServiceMeta.set_layouts([])


class ClusterResource(CloudServiceResource):
    cloud_service_group = StringType(default="Cluster")


class EventResource(ClusterResource):
    cloud_service_type = StringType(default="Event")
    data = ModelType(Event)
    _metadata = ModelType(
        CloudServiceMeta, default=event_meta, serialized_name="metadata"
    )


class EventResponse(CloudServiceResponse):
    resource = PolyModelType(EventResource)
