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


class NamespaceCondition(Model):
    lastTransitionTime = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NamespaceStatus(Model):
    conditions = ListType(ModelType(NamespaceCondition), serialize_when_none=False)
    phase = StringType(choices=("Active", "Terminating"), serialize_when_none=False)


class NamespaceSpec(Model):
    finalizers = ListType(StringType(), serialize_when_none=False)


class Namespace(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(NamespaceSpec, serialize_when_none=False)
    status = ModelType(NamespaceStatus, serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
