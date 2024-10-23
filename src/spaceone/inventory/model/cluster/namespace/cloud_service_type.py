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

cst_namespace = CloudServiceTypeResource()
cst_namespace.name = "Namespace"
cst_namespace.provider = "k8s"
cst_namespace.group = "Cluster"
cst_namespace.service_code = "Namespace"
cst_namespace.is_primary = True
cst_namespace.is_major = False
cst_namespace.labels = ["Container"]
cst_namespace.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/namespace.svg",
}

cst_namespace._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source(
            "Status",
            "data.status.phase",
            default_badge={"green.500": ["Active"], "red.500": ["Terminating"]},
        ),
        TextDyField.data_source("Cluster", "account"),
        DateTimeDyField.data_source("Created", "data.metadata.creation_timestamp"),
        TextDyField.data_source("Uid", "data.uid", options={"is_optional": True}),
    ],
    search=[
        SearchField.set(name="Uid", key="data.uid"),
        SearchField.set(name="Status", key="data.status.phase"),
        SearchField.set(name="Cluster", key="account"),
        SearchField.set(name="Created", key="data.metadata.creation_timestamp"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_namespace}),
]
