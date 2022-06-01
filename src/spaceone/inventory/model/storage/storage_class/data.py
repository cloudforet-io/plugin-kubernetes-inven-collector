from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, Condition


class TopologySelectorLabelRequirement(Model):
    key = StringType(serialize_when_none=False)
    values = ListType(StringType(), serialize_when_none=False)


class TopologySelectorTerm(Model):
    match_label_expressions = ListType(ModelType(TopologySelectorLabelRequirement), serialize_when_none=False)


class StorageClass(Model):
    allow_volume_expansion = BooleanType(serialize_when_none=False)
    allowed_topologies = ListType(ModelType(TopologySelectorTerm), serialize_when_none=False)
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    mount_options = ListType(StringType(), serialize_when_none=False)
    parameters = DictType(StringType(), serialize_when_none=False)
    provisioner = StringType(serialize_when_none=False)
    reclaim_policy = StringType(serialize_when_none=False)
    

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
