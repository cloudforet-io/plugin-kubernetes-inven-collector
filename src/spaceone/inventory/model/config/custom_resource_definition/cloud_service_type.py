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

cst_custom_resource_definition = CloudServiceTypeResource()
cst_custom_resource_definition.name = "CustomResourceDefinition"
cst_custom_resource_definition.provider = "k8s"
cst_custom_resource_definition.group = "Config"
cst_custom_resource_definition.service_code = "CustomResourceDefinition"
cst_custom_resource_definition.is_primary = False
cst_custom_resource_definition.is_major = False
cst_custom_resource_definition.labels = ["Application Integration"]
cst_custom_resource_definition.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/custom_resource_definition.svg",
}

cst_custom_resource_definition._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Group", "data.spec.group"),
        TextDyField.data_source("Scope", "data.spec.scope"),
        TextDyField.data_source("Age", "data.age"),
        TextDyField.data_source("Cluster", "account"),
        TextDyField.data_source("Generation", "data.metadata.generation"),
        DateTimeDyField.data_source(
            "Start Time",
            "data.metadata.creation_timestamp",
            options={"is_optional": True},
        ),
        TextDyField.data_source("Uid", "data.uid", options={"is_optional": True}),
    ],
    search=[
        SearchField.set(name="Uid", key="data.uid"),
        SearchField.set(name="Scope", key="data.spec.scope"),
        SearchField.set(name="Group", key="data.spec.group"),
        SearchField.set(name="Age", key="data.age"),
        SearchField.set(name="Cluster", key="account"),
        SearchField.set(name="Generation", key="data.metadata.generation"),
        SearchField.set(name="Start Time", key="data.metadata.creation_timestamp"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_custom_resource_definition}),
]
