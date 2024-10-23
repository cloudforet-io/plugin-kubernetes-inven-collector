import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import (
    CardWidget,
)
from spaceone.inventory.libs.schema.metadata.dynamic_field import (
    TextDyField,
    SearchField,
    DateTimeDyField,
    EnumDyField,
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

cst_pod = CloudServiceTypeResource()
cst_pod.name = "Pod"
cst_pod.provider = "k8s"
cst_pod.group = "WorkLoad"
cst_pod.service_code = "Pod"
cst_pod.is_primary = True
cst_pod.is_major = True
cst_pod.labels = ["Container"]
cst_pod.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/pod.svg",
}

cst_pod._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Containers", "data.containers"),
        EnumDyField.data_source(
            "Status",
            "data.status.phase",
            default_state={
                "safe": ["Running", "Succeeded"],
                "alert": ["Pending", "Failed", "Unknown"],
            },
        ),
        TextDyField.data_source("Age", "data.age"),
        TextDyField.data_source("Restarts", "data.restarts"),
        TextDyField.data_source("Namespace", "data.metadata.namespace"),
        TextDyField.data_source("Node Name", "data.spec.node_name"),
        TextDyField.data_source("Cluster", "account"),
        TextDyField.data_source(
            "Pod IP", "data.status.pod_ip", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Host IP", "data.status.host_ip", options={"is_optional": True}
        ),
        DateTimeDyField.data_source(
            "Start Time", "data.status.start_time", options={"is_optional": True}
        ),
        TextDyField.data_source("Uid", "data.uid", options={"is_optional": True}),
        TextDyField.data_source(
            "QoS", "data.status.qos_class", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Uid", key="data.uid"),
        SearchField.set(name="Namespace", key="data.metadata.namespace"),
        SearchField.set(name="Cluster", key="account"),
        SearchField.set(name="Pod IP", key="data.status.pod_ip"),
        SearchField.set(name="Node Name", key="data.spec.node_name"),
        SearchField.set(name="Host IP", key="data.status.host_ip"),
        SearchField.set(name="Start Time", key="data.status.start_time"),
        SearchField.set(name="QoS", key="data.status.qos_class"),
        SearchField.set(name="Restarts", key="data.restarts"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_pod}),
]
