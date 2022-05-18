from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, PodTemplateSpec


class RollingUpdateDaemonSet(Model):
    max_surge = StringType(serialize_when_none=False)
    max_unavailable = StringType(serialize_when_none=False)


class DaemonSetUpdateStrategy(Model):
    rolling_update = ModelType(RollingUpdateDaemonSet, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class DaemonSetSpec(Model):
    min_ready_seconds = IntType(serialize_when_none=False)
    revision_history_limit = IntType(serialize_when_none=False)
    selector = ModelType(LabelSelector, serialize_when_none=False)
    template = ModelType(PodTemplateSpec, serialize_when_none=False)
    update_strategy = ModelType(DaemonSetUpdateStrategy, serialize_when_none=False)


class DaemonSetCondition(Model):
    last_transition_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class DaemonSetStatus(Model):
    collision_count = IntType(serialize_when_none=False)
    conditions = ListType(ModelType(DaemonSetCondition), serialize_when_none=False)
    current_number_scheduled = IntType(serialize_when_none=False)
    desired_number_scheduled = IntType(serialize_when_none=False)
    number_available = IntType(serialize_when_none=False)
    number_mis_scheduled = IntType(serialize_when_none=False)
    number_ready = IntType(serialize_when_none=False)
    number_unavailable = IntType(serialize_when_none=False)
    observed_generation = IntType(serialize_when_none=False)
    updated_number_scheduled = IntType(serialize_when_none=False)


class DaemonSet(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(DaemonSetSpec, serialize_when_none=False)
    status = ModelType(DaemonSetStatus, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
