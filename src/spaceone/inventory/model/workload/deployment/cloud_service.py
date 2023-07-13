from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.workload.deployment.data import Deployment
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
Deployment
"""

deployment_metadata_base_meta = ItemDynamicLayout.set_fields(
    "Metadata",
    root_path="data",
    fields=[
        DateTimeDyField.data_source("Created", "metadata.creation_timestamp"),
        TextDyField.data_source("Name", "metadata.name"),
        TextDyField.data_source("Namespace", "metadata.namespace"),
        TextDyField.data_source("Replicas", "spec.replicas"),
        TextDyField.data_source("Selector", "spec.selector"),
        TextDyField.data_source("Node Selector", "spec.template.spec.node_selector"),
        TextDyField.data_source("Strategy Type", "spec.strategy"),
    ],
)

deployment_status_conditions_meta = SimpleTableDynamicLayout.set_fields(
    "Conditions",
    root_path="data.status.conditions",
    fields=[
        TextDyField.data_source("Type", "type"),
        TextDyField.data_source("Status", "status"),
        TextDyField.data_source("Message", "message"),
        TextDyField.data_source("Reason", "reason"),
        DateTimeDyField.data_source("Last Probe Time", "last_probe_time"),
        DateTimeDyField.data_source("Last Transition Time", "last_transition_time"),
    ],
)

deployment_metadata_meta = ListDynamicLayout.set_layouts(
    "Metadata",
    layouts=[deployment_metadata_base_meta, deployment_status_conditions_meta],
)

deployment_pods = TableDynamicLayout.set_fields(
    "Pods",
    root_path="data.pods",
    fields=[
        TextDyField.data_source("Name", "metadata.name"),
        EnumDyField.data_source(
            "Status",
            "status.phase",
            default_state={
                "safe": ["Running", "Succeeded"],
                "alert": ["Pending", "Failed", "Unknown"],
            },
        ),
        TextDyField.data_source("Containers", "containers"),
        TextDyField.data_source("Namespace", "metadata.namespace"),
        TextDyField.data_source("Node Name", "spec.node_name"),
        TextDyField.data_source("Age", "age"),
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

deployment_meta = CloudServiceMeta.set_layouts(
    [deployment_metadata_meta, deployment_pods, annotations, labels]
)


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default="WorkLoad")


class DeploymentResource(WorkLoadResource):
    cloud_service_type = StringType(default="Deployment")
    data = ModelType(Deployment)
    _metadata = ModelType(
        CloudServiceMeta, default=deployment_meta, serialized_name="metadata"
    )


class DeploymentResponse(CloudServiceResponse):
    resource = PolyModelType(DeploymentResource)
