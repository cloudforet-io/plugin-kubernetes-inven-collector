from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, ObjectReference


class NodeCondition(Model):
    name = StringType(serialize_when_none=False)
    last_heartbeat_time = DateTimeType(serialize_when_none=False)
    last_transition_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = BooleanType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Cluster(Model):
    uid = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    state = StringType(serialize_when_none=False)
    kubernetes_provider = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    cpu_total = FloatType(serialize_when_none=False)
    cpu_assigned = FloatType(serialize_when_none=False)
    memory_total = IntType(serialize_when_none=False)
    memory_assigned = IntType(serialize_when_none=False)
    pod_total = IntType(serialize_when_none=False)
    pod_assigned = IntType(serialize_when_none=False)
    node_conditions = ListType(ModelType(NodeCondition), serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
