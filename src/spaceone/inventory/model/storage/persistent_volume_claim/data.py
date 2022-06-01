from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, Condition, PersistentVolumeClaimSpec


class PersistentVolumeClaimCondition(Model):
    last_probe_time = DateTimeType(serialize_when_none=False)
    last_transition_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PersistentVolumeClaimStatus(Model):
    access_modes = ListType(StringType(), serialize_when_none=False)
    allocated_resources = DictType(StringType, serialize_when_none=False)
    capacity = DictType(StringType, serialize_when_none=False)
    conditions = ListType(ModelType(PersistentVolumeClaimCondition), serialize_when_none=False)
    phase = StringType(serialize_when_none=False)
    resize_status = StringType(serialize_when_none=False)


class PersistentVolumeClaim(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(PersistentVolumeClaimSpec, serialize_when_none=False)
    status = ModelType(PersistentVolumeClaimStatus, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
