from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cluster.cluster.data import Cluster
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
Cluster
"""

cluster = ItemDynamicLayout.set_fields(
    "Cluster",
    fields=[
        TextDyField.data_source("Name", "name"),
        EnumDyField.data_source(
            "Status",
            "data.state",
            default_badge={"green.500": ["Ready"], "red.500": ["NotReady"]},
        ),
        TextDyField.data_source("Version", "data.version"),
        TextDyField.data_source("Kubernetes Provider", "data.kubernetes_provider"),
        TextDyField.data_source("CPU Assigned", "data.cpu_assigned"),
        TextDyField.data_source("CPU Total", "data.cpu_total"),
        TextDyField.data_source("Memory Assigned", "data.memory_assigned"),
        TextDyField.data_source("Memory Total", "data.memory_total"),
        TextDyField.data_source("Pod Assigned", "data.pod_assigned"),
        TextDyField.data_source("Pod Total", "data.pod_total"),
    ],
)

cluster_condition = TableDynamicLayout.set_fields(
    "Condition",
    root_path="data.node_conditions",
    fields=[
        TextDyField.data_source("Type", "type"),
        TextDyField.data_source("Name", "name"),
        EnumDyField.data_source(
            "Status",
            "state",
            default_badge={"green.500": ["true"], "red.500": ["false"]},
        ),
        TextDyField.data_source("Message", "message"),
        TextDyField.data_source("Reason", "reason"),
        DateTimeDyField.data_source("Last Heartbeat Time", "last_heartbeat_time"),
        DateTimeDyField.data_source("Last Transition Time", "last_transition_time"),
    ],
)

cluster_meta = CloudServiceMeta.set_layouts([cluster, cluster_condition])


class ClusterGroupResource(CloudServiceResource):
    cloud_service_group = StringType(default="Cluster")


class ClusterResource(ClusterGroupResource):
    cloud_service_type = StringType(default="Cluster")
    data = ModelType(Cluster)
    _metadata = ModelType(
        CloudServiceMeta, default=cluster_meta, serialized_name="metadata"
    )


class ClusterResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterResource)
