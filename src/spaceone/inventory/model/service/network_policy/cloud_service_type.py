import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import (
    CardWidget,
    ChartWidget,
)
from spaceone.inventory.libs.schema.metadata.dynamic_field import (
    TextDyField,
    SearchField,
    DateTimeDyField,
    ListDyField,
    EnumDyField,
    SizeField,
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

cst_network_policy = CloudServiceTypeResource()
cst_network_policy.name = "NetworkPolicy"
cst_network_policy.provider = "kubernetes"
cst_network_policy.group = "Service"
cst_network_policy.service_code = "NetworkPolicy"
cst_network_policy.is_primary = True
cst_network_policy.is_major = False
cst_network_policy.labels = ["Networking"]
cst_network_policy.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/network_policy.svg",
}

cst_network_policy._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Cluster", "account"),
        DateTimeDyField.data_source("Start Time", "data.metadata.creation_timestamp"),
        TextDyField.data_source("Uid", "data.uid", options={"is_optional": True}),
    ],
    search=[
        SearchField.set(name="Uid", key="data.uid"),
        SearchField.set(name="Cluster", key="account"),
        SearchField.set(name="Start Time", key="data.metadata.creation_timestamp"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_network_policy}),
]
