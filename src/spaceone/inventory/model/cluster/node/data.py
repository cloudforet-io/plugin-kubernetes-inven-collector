from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, PodTemplateSpec


class ConfigMapNodeConfigSource(Model):
    kubeletConfigKey = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)
    resourceVersion = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)


class NodeConfigSource(Model):
    configMap = ModelType(ConfigMapNodeConfigSource, serialize_when_none=False)


class Taint(Model):
    effect = StringType(serialize_when_none=False)
    key = StringType(serialize_when_none=False)
    timeAdded = DateTimeType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class NodeSpec(Model):
    configSource = ModelType(NodeConfigSource, serialize_when_none=False)
    externalID = StringType(serialize_when_none=False)
    podCIDR = StringType(serialize_when_none=False)
    podCIDRs = ListType(StringType(), serialize_when_none=False)
    providerID = StringType(serialize_when_none=False)
    taints = ListType(ModelType(Taint), serialize_when_none=False)
    unschedulable = BooleanType(serialize_when_none=False)


class NodeAddress(Model):
    address = StringType()
    type = StringType()


class NodeCondition(Model):
    lastHeartbeatTime = DateTimeType(serialize_when_none=False)
    lastTransitionTime = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NodeConfigStatus(Model):
    active = ModelType(NodeConfigSource, serialize_when_none=False)
    assigned = ModelType(NodeConfigSource, serialize_when_none=False)
    error = StringType(serialize_when_none=False)
    lastKnownGood = ModelType(NodeConfigSource, serialize_when_none=False)


class DaemonEndpoint(Model):
    Port = IntType(serialize_when_none=False)


class NodeDaemonEndpoints(Model):
    kubeletEndpoint = ModelType(DaemonEndpoint, serialize_when_none=False)


class ContainerImage(Model):
    names = ListType(StringType(), serialize_when_none=False)
    sizeBytes = IntType(serialize_when_none=False)


class NodeSystemInfo(Model):
    architecture = StringType(serialize_when_none=False)
    bootID = StringType(serialize_when_none=False)
    containerRuntimeVersion = StringType(serialize_when_none=False)
    kernelVersion = StringType(serialize_when_none=False)
    kubeProxyVersion = StringType(serialize_when_none=False)
    kubeletVersion = StringType(serialize_when_none=False)
    machineID = StringType(serialize_when_none=False)
    operatingSystem = StringType(serialize_when_none=False)
    osImage = StringType(serialize_when_none=False)
    systemUUID = StringType(serialize_when_none=False)


class AttachedVolume(Model):
    devicePath = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class NodeStatus(Model):
    addresses = ListType(ModelType(NodeAddress), serialize_when_none=False)
    allocatable = DictType(StringType(), serialize_when_none=False)
    capacity = DictType(StringType(), serialize_when_none=False)
    conditions = ListType(ModelType(NodeCondition), serialize_when_none=False)
    config = ListType(ModelType(NodeConfigStatus), serialize_when_none=False)
    daemonEndpoints = ModelType(NodeDaemonEndpoints, serialize_when_none=False)
    images = ListType(ModelType(ContainerImage), serialize_when_none=False)
    nodeInfo = ModelType(NodeSystemInfo, serialize_when_none=False)
    phase = StringType(serialize_when_none=False)
    volumesAttached = ListType(ModelType(AttachedVolume), serialize_when_none=False)
    volumesInUse = ListType(StringType(), serialize_when_none=False)


class Node(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(NodeSpec, serialize_when_none=False)
    status = ModelType(NodeStatus, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
