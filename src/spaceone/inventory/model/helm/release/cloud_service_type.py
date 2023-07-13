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

cst_release = CloudServiceTypeResource()
cst_release.name = "Release"
cst_release.provider = "kubernetes"
cst_release.group = "Helm"
cst_release.service_code = "Release"
cst_release.is_primary = True
cst_release.is_major = True
cst_release.labels = ["Application Integration"]
cst_release.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/release.svg",
}

cst_release._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Cluster", "account"),
        TextDyField.data_source("Status", "data.data.release.info.status"),
        TextDyField.data_source("Version", "data.data.release.version"),
        TextDyField.data_source("Chart Name", "data.data.release.chart.metadata.name"),
        TextDyField.data_source("Home", "data.data.release.chart.metadata.home"),
        TextDyField.data_source(
            "App Version", "data.data.release.chart.metadata.app_version"
        ),
        DateTimeDyField.data_source("Start Time", "data.metadata.creation_timestamp"),
    ],
    search=[
        SearchField.set(name="Cluster", key="account"),
        SearchField.set(name="Status", key="data.data.release.info.status"),
        SearchField.set(name="Version", key="data.data.release.version"),
        SearchField.set(name="Chart Name", key="metadata.name"),
        SearchField.set(name="Home", key="metadata.home"),
        SearchField.set(name="App Version", key="metadata.app_version"),
        SearchField.set(name="Start Time", key="data.metadata.creation_timestamp"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_release}),
]
