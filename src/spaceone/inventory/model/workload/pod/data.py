from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, PodSpec


class PodCondition(Model):
    last_probe_time = DateTimeType(serialize_when_none=False)
    last_transition_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ContainerStateRunning(Model):
    started_at = DateTimeType(serialize_when_none=False)


class ContainerStateTerminated(Model):
    container_id = StringType(serialize_when_none=False)
    exit_code = IntType(serialize_when_none=False)
    finished_at = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    signal = IntType(serialize_when_none=False)
    started_at = DateTimeType(serialize_when_none=False)


class ContainerStateWaiting(Model):
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)


class ContainerState(Model):
    running = ModelType(ContainerStateRunning, serialize_when_none=False)
    terminated = ModelType(ContainerStateTerminated, serialize_when_none=False)
    waiting = ModelType(ContainerStateWaiting, serialize_when_none=False)


class ContainerStatus(Model):
    container_id = StringType(serialize_when_none=False)
    image = StringType(serialize_when_none=False)
    image_id = StringType(serialize_when_none=False)
    last_state = ModelType(ContainerState, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    ready = BooleanType(serialize_when_none=False)
    restart_count = IntType(serialize_when_none=False)
    started = BooleanType(serialize_when_none=False)
    state = ModelType(ContainerState, serialize_when_none=False)


class PodIP(Model):
    ip = StringType(serialize_when_none=False)


class PodStatus(Model):
    conditions = ListType(ModelType(PodCondition), serialize_when_none=False)
    container_statuses = ListType(ModelType(ContainerStatus), serialize_when_none=False)
    ephemeral_container_statuses = ListType(ModelType(ContainerStatus), serialize_when_none=False)
    init_container_statuses = ListType(ModelType(ContainerStatus), serialize_when_none=False)
    host_ip = StringType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    nominated_node_name = StringType(serialize_when_none=False)
    phase = StringType(choices=('Running', 'Succeeded', 'Pending', 'Failed', 'Unknown'), serialize_when_none=False)
    pod_ip = StringType(serialize_when_none=False)
    pod_i_ps = ListType(ModelType(PodIP), serialize_when_none=False)
    qos_class = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    start_time = DateTimeType(serialize_when_none=False)


class Pod(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(PodSpec, serialize_when_none=False)
    status = ModelType(PodStatus, serialize_when_none=False)
    restarts = IntType(serialize_when_none=False)
    age = StringType(serialize_when_none=False)
    containers = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
