from schematics import Model
from schematics.types import (
    ModelType,
    ListType,
    StringType,
    DateTimeType,
    IntType,
    BooleanType,
)

from spaceone.inventory.libs.schema.base import (
    ObjectMeta,
    LabelSelector,
    PodTemplateSpec,
    PodFailurePolicy,
    UncountedTerminatedPods,
    ListMeta,
)
from spaceone.inventory.model.workload.pod.data import Pod


class JobCondition(Model):
    lastProbeTime = DateTimeType(serialize_when_none=False)
    lastTransitionTime = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class JobStatus(Model):
    active = IntType(serialize_when_none=False)
    completedIndexes = StringType(serialize_when_none=False)
    completionTime = DateTimeType(serialize_when_none=False)
    conditions = ListType(ModelType(JobCondition), serialize_when_none=False)
    failed = IntType(serialize_when_none=False)
    ready = IntType(serialize_when_none=False)
    startTime = DateTimeType(serialize_when_none=False)
    succeeded = IntType(serialize_when_none=False)
    uncountedTerminatedPods = ModelType(
        UncountedTerminatedPods, serialize_when_none=False
    )


class JobSpec(Model):
    activeDeadlineSeconds = IntType(serialize_when_none=False)
    backoffLimit = IntType(serialize_when_none=False)
    completionMode = StringType(serialize_when_none=False)
    completions = IntType(serialize_when_none=False)
    manualSelector = BooleanType(serialize_when_none=False)
    parallelism = IntType(serialize_when_none=False)
    podFailurePolicy = ModelType(PodFailurePolicy, serialize_when_none=False)
    selector = ModelType(LabelSelector, serialize_when_none=False)
    suspend = BooleanType(serialize_when_none=False)
    template = ModelType(PodTemplateSpec, serialize_when_none=False)
    ttlSecondsAfterFinished = IntType(serialize_when_none=False)


class Job(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(JobSpec, serialize_when_none=False)
    status = ModelType(JobStatus, serialize_when_none=False)
    age = StringType(serialize_when_none=False)
    pods = ListType(ModelType(Pod), serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": ""}


class JobList(Model):
    api_version = StringType(serialize_when_none=False)
    items = ListType(ModelType(Job), serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ListMeta, serialize_when_none=False)
