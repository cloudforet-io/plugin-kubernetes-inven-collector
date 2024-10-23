import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import (
    CardWidget,
)
from spaceone.inventory.libs.schema.metadata.dynamic_field import (
    TextDyField,
    SearchField,
    DateTimeDyField,
)
from spaceone.inventory.libs.schema.cloud_service_type import (
    CloudServiceTypeResource,
    CloudServiceTypeResponse,
    CloudServiceTypeMeta,
)

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, "widget/total_count.yml")
count_by_region_conf = os.path.join(current_dir, "widget/count_by_region.yml")
count_by_cluster_conf = os.path.join(current_dir, "widget/count_by_cluster.yml")

cst_deployment = CloudServiceTypeResource()
cst_deployment.name = "Deployment"
cst_deployment.provider = "k8s"
cst_deployment.group = "WorkLoad"
cst_deployment.service_code = "Deployment"
cst_deployment.is_primary = True
cst_deployment.is_major = True
cst_deployment.labels = ["Container"]
cst_deployment.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/deployment.svg",
}

cst_deployment._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Namespace", "data.metadata.namespace"),
        TextDyField.data_source("Cluster", "account"),
        TextDyField.data_source("Ready", "data.ready"),
        TextDyField.data_source("Age", "data.age"),
        DateTimeDyField.data_source("Start Time", "data.metadata.creation_timestamp"),
        TextDyField.data_source(
            "Available Replicas",
            "data.status.ready_replicas",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Target Replicas", "data.status.replicas", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Strategy", "data.spec.strategy.type", options={"is_optional": True}
        ),
        TextDyField.data_source("Uid", "data.uid", options={"is_optional": True}),
    ],
    search=[
        SearchField.set(name="Uid", key="data.uid"),
        SearchField.set(name="Namespace", key="data.namespace"),
        SearchField.set(name="Cluster", key="account"),
        SearchField.set(name="Ready", key="data.ready"),
        SearchField.set(name="Age", key="data.age"),
        SearchField.set(name="Available Replicas", key="data.status.ready_replicas"),
        SearchField.set(name="Target Replicas", key="data.status.replicas"),
        SearchField.set(name="Strategy", key="data.spec.strategy.type"),
        SearchField.set(name="Start Time", key="data.status.start_time"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_deployment}),
]
