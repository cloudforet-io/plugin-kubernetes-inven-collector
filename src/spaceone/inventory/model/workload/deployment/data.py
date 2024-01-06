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
    PodSpec,
    LabelSelector,
    PodTemplateSpec,
)
from spaceone.inventory.model.workload.pod.data import Pod


class RollingUpdateDeployment(Model):
    max_surge = StringType(serialize_when_none=False)
    max_unavailable = StringType(serialize_when_none=False)


class DeploymentStrategy(Model):
    rolling_update = ModelType(RollingUpdateDeployment, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class DeploymentSpec(Model):
    min_ready_seconds = IntType(serialize_when_none=False)
    paused = BooleanType(serialize_when_none=False)
    progress_deadline_seconds = IntType(serialize_when_none=False)
    replicas = IntType(serialize_when_none=False)
    revision_history_limit = IntType(serialize_when_none=False)
    selector = ModelType(LabelSelector, serialize_when_none=False)
    strategy = ModelType(DeploymentStrategy, serialize_when_none=False)
    template = ModelType(PodTemplateSpec)


class DeploymentCondition(Model):
    last_transition_time = DateTimeType(serialize_when_none=False)
    last_update_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class DeploymentStatus(Model):
    available_replicas = IntType(serialize_when_none=False)
    collision_count = IntType(serialize_when_none=False)
    conditions = ListType(ModelType(DeploymentCondition), serialize_when_none=False)
    observed_generation = IntType(serialize_when_none=False)
    ready_replicas = IntType(serialize_when_none=False)
    replicas = IntType(serialize_when_none=False)
    unavailable_replicas = IntType(serialize_when_none=False)
    updated_replicas = IntType(serialize_when_none=False)


class Deployment(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(DeploymentSpec, serialize_when_none=False)
    status = ModelType(DeploymentStatus, serialize_when_none=False)
    ready = StringType(serialized_name=False)
    age = StringType(serialize_when_none=False)
    pods = ListType(ModelType(Pod), serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
