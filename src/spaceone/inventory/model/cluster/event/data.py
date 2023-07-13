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
from spaceone.inventory.libs.schema.base import ObjectMeta, ObjectReference


class EventSeries(Model):
    count = IntType(serialize_when_none=False)
    lastObservedTime = DateTimeType(serialize_when_none=False)


class Event(Model):
    api_version = StringType(serialize_when_none=False)
    action = StringType(serialize_when_none=False)
    eventTime = DateTimeType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    note = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    regarding = ModelType(ObjectReference, serialize_when_none=False)
    related = ModelType(ObjectReference, serialize_when_none=False)
    reportingController = StringType(serialize_when_none=False)
    reportingInstance = StringType(serialize_when_none=False)
    series = ModelType(EventSeries, serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
