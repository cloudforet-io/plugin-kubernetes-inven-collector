import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import (
    CardWidget,
)
from spaceone.inventory.libs.schema.metadata.dynamic_field import (
    TextDyField,
    SearchField,
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

cst_cluster = CloudServiceTypeResource()
cst_cluster.name = "Cluster"
cst_cluster.provider = "k8s"
cst_cluster.group = "Cluster"
cst_cluster.service_code = "Cluster"
cst_cluster.is_primary = True
cst_cluster.is_major = True
cst_cluster.labels = ["Container"]
cst_cluster.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/cluster.svg",
}

cst_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source(
            "Status",
            "data.state",
            default_badge={"green.500": ["Ready"], "red.500": ["NotReady"]},
        ),
        TextDyField.data_source("Version", "data.version"),
        TextDyField.data_source("Kubernetes Provider", "data.kubernetes_provider"),
        TextDyField.data_source(
            "CPU Assigned", "data.cpu_assigned", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "CPU Total", "data.cpu_total", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Memory Assigned", "data.memory_assigned", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Memory Total", "data.memory_total", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Pod Assigned", "data.pod_assigned", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Pod Total", "data.pod_total", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Status", key="data.state"),
        SearchField.set(name="Version", key="data.version"),
        SearchField.set(name="Kubernetes Provider", key="data.kubernetes_provider"),
        SearchField.set(name="CPU Assigned", key="data.cpu_assigned"),
        SearchField.set(name="CPU Total", key="data.cpu_total"),
        SearchField.set(name="Memory Assigned", key="data.memory_assigned"),
        SearchField.set(name="Memory Total", key="data.memory_total"),
        SearchField.set(name="Pod Assigned", key="data.pod_assigned"),
        SearchField.set(name="Pod Total", key="data.pod_total"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_cluster}),
]
