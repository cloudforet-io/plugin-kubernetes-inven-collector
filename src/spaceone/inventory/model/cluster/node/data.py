from schematics import Model
from schematics.types import (
    ModelType,
    ListType,
    StringType,
    FloatType,
    DateTimeType,
    IntType,
    BooleanType,
    DictType,
)
from spaceone.inventory.libs.schema.base import (
    ObjectMeta,
    LabelSelector,
    PodTemplateSpec,
)


class ConfigMapNodeConfigSource(Model):
    kubelet_config_key = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)
    resource_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)


class NodeConfigSource(Model):
    config_map = ModelType(ConfigMapNodeConfigSource, serialize_when_none=False)


class Taint(Model):
    effect = StringType(serialize_when_none=False)
    key = StringType(serialize_when_none=False)
    time_added = DateTimeType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class NodeSpec(Model):
    config_source = ModelType(NodeConfigSource, serialize_when_none=False)
    external_id = StringType(serialize_when_none=False)
    pod_cidr = StringType(serialize_when_none=False)
    pod_cidrs = ListType(StringType(), serialize_when_none=False)
    provider_id = StringType(serialize_when_none=False)
    taints = ListType(ModelType(Taint), serialize_when_none=False)
    unschedulable = BooleanType(serialize_when_none=False)


class NodeAddress(Model):
    address = StringType()
    type = StringType()


class NodeCondition(Model):
    last_heartbeat_time = DateTimeType(serialize_when_none=False)
    last_transition_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NodeConfigStatus(Model):
    active = ModelType(NodeConfigSource, serialize_when_none=False)
    assigned = ModelType(NodeConfigSource, serialize_when_none=False)
    error = StringType(serialize_when_none=False)
    lastKnown_good = ModelType(NodeConfigSource, serialize_when_none=False)


class DaemonEndpoint(Model):
    port = IntType(serialize_when_none=False)


class NodeDaemonEndpoints(Model):
    kubelet_endpoint = ModelType(DaemonEndpoint, serialize_when_none=False)


class ContainerImage(Model):
    names = ListType(StringType(), serialize_when_none=False)
    size_bytes = IntType(serialize_when_none=False)


class NodeSystemInfo(Model):
    architecture = StringType(serialize_when_none=False)
    boot_id = StringType(serialize_when_none=False)
    container_runtime_version = StringType(serialize_when_none=False)
    kernel_version = StringType(serialize_when_none=False)
    kube_proxy_version = StringType(serialize_when_none=False)
    kubelet_version = StringType(serialize_when_none=False)
    machine_id = StringType(serialize_when_none=False)
    operating_system = StringType(serialize_when_none=False)
    os_image = StringType(serialize_when_none=False)
    system_uuid = StringType(serialize_when_none=False)


class AttachedVolume(Model):
    device_path = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class NodeStatus(Model):
    addresses = ListType(ModelType(NodeAddress), serialize_when_none=False)
    allocatable = DictType(StringType(), serialize_when_none=False)
    capacity = DictType(StringType(), serialize_when_none=False)
    conditions = ListType(ModelType(NodeCondition), serialize_when_none=False)
    config = ListType(ModelType(NodeConfigStatus), serialize_when_none=False)
    daemon_endpoints = ModelType(NodeDaemonEndpoints, serialize_when_none=False)
    images = ListType(ModelType(ContainerImage), serialize_when_none=False)
    node_info = ModelType(NodeSystemInfo, serialize_when_none=False)
    phase = StringType(serialize_when_none=False)
    volumes_attached = ListType(ModelType(AttachedVolume), serialize_when_none=False)
    volumes_in_use = ListType(StringType(), serialize_when_none=False)


class Display(Model):
    status = StringType(choices=("Ready", "NotReady"), serialize_when_none=False)


class Node(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    display = ModelType(Display, serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(NodeSpec, serialize_when_none=False)
    status = ModelType(NodeStatus, serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
