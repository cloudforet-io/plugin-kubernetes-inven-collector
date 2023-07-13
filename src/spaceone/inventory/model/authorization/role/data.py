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
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, PolicyRule


class Role(Model):
    api_version = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    rules = ListType(ModelType(PolicyRule), serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
