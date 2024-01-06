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


class CertificateSigningRequestCondition(Model):
    last_transition_time = DateTimeType(serialize_when_none=False)
    last_update_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class CertificateSigningRequestStatus(Model):
    certificate = StringType(serialize_when_none=False)
    conditions = ListType(
        ModelType(CertificateSigningRequestCondition), serialize_when_none=False
    )


class CertificateSigningRequestSpec(Model):
    expiration_seconds = IntType(serialize_when_none=False)
    extra = DictType(StringType(), serialize_when_none=False)
    groups = ListType(StringType(), serialize_when_none=False)
    request = StringType(serialize_when_none=False)
    signer_name = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    usages = ListType(StringType(), serialize_when_none=False)
    username = StringType(serialize_when_none=False)


class CertificateSigningRequest(Model):
    api_version = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(CertificateSigningRequestSpec, serialize_when_none=False)
    status = ModelType(CertificateSigningRequestStatus, serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
