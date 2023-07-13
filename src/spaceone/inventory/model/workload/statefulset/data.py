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
from spaceone.inventory.model.storage.persistent_volume_claim.data import (
    PersistentVolumeClaim,
)
from spaceone.inventory.model.workload.pod.data import Pod


class StatefulSetPersistentVolumeClaimRetentionPolicy(Model):
    whenDeleted = StringType(serialize_when_none=False)
    whenScaled = StringType(serialize_when_none=False)


class RollingUpdateStatefulSetStrategy(Model):
    maxUnavailable = StringType(serialize_when_none=False)
    partition = IntType(serialize_when_none=False)


class StatefulSetUpdateStrategy(Model):
    rollingUpdate = ModelType(
        RollingUpdateStatefulSetStrategy, serialize_when_none=False
    )
    type = StringType(serialize_when_none=False)


class StatefulSetSpec(Model):
    minReadySeconds = IntType(serialize_when_none=False)
    persistentVolumeClaimRetentionPolicy = ModelType(
        StatefulSetPersistentVolumeClaimRetentionPolicy, serialize_when_none=False
    )
    podManagementPolicy = StringType(serialize_when_none=False)
    replicas = IntType(serialize_when_none=False)
    revisionHistoryLimit = IntType(serialize_when_none=False)
    selector = ListType(ModelType(LabelSelector), serialize_when_none=False)
    serviceName = StringType(serialize_when_none=False)
    template = ModelType(PodTemplateSpec, serialize_when_none=False)
    updateStrategy = ModelType(StatefulSetUpdateStrategy, serialize_when_none=False)
    volumeClaimTemplates = ListType(
        ModelType(PersistentVolumeClaim), serialize_when_none=False
    )


class StatefulSetCondition(Model):
    lastTransitionTime = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class StatefulSetStatus(Model):
    availableReplicas = IntType(serialize_when_none=False)
    collisionCount = IntType(serialize_when_none=False)
    conditions = ListType(ModelType(StatefulSetCondition), serialize_when_none=False)
    currentReplicas = IntType(serialize_when_none=False)
    currentRevision = StringType(serialize_when_none=False)
    observedGeneration = IntType(serialize_when_none=False)
    readyReplicas = IntType(serialize_when_none=False)
    replicas = IntType(serialize_when_none=False)
    updateRevision = StringType(serialize_when_none=False)
    updatedReplicas = IntType(serialize_when_none=False)


class StatefulSet(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(StatefulSetSpec, serialize_when_none=False)
    status = ModelType(StatefulSetStatus, serialize_when_none=False)
    age = StringType(serialize_when_none=False)
    pods = ListType(ModelType(Pod), serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
