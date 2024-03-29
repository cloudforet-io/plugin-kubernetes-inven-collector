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
    LocalObjectReference,
    ObjectReference,
)


class SecretData(Model):
    key = StringType(serialized_name=False)
    value = StringType(serialized_name=False)


class Secret(Model):
    api_version = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    immutable = BooleanType(serialize_when_none=False)
    age = StringType(serialize_when_none=False)
    keys = StringType(serialized_name=False)
    data = ListType(ModelType(SecretData), serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
