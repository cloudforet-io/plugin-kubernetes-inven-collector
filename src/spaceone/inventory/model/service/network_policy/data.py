from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, Condition


class IPBlock(Model):
    cidr = StringType(serialize_when_none=False)
    # Reserved python keyword
    except_ = ListType(StringType(), deserialize_from='except', serialize_when_none=False)


class NetworkPolicyPeer(Model):
    ip_block = ModelType(IPBlock, serialize_when_none=False)
    namespace_selector = ListType(ModelType(LabelSelector), serialize_when_none=False)
    pod_selector = ListType(ModelType(LabelSelector), serialize_when_none=False)


class NetworkPolicyPort(Model):
    end_port = IntType(serialize_when_none=False)
    port = StringType(serialize_when_none=False)
    protocol = StringType(serialize_when_none=False)


class NetworkPolicyEgressRule(Model):
    ports = ListType(ModelType(NetworkPolicyPort), serialize_when_none=False)
    to = ListType(ModelType(NetworkPolicyPeer), serialize_when_none=False)


class NetworkPolicyIngressRule(Model):
    # Reserved python keyword
    from_ = ListType(ModelType(NetworkPolicyPeer), deserialize_from='from', serialize_when_none=False)
    ports = ListType(ModelType(NetworkPolicyPort), serialize_when_none=False)


class NetworkPolicySpec(Model):
    egress = ListType(ModelType(NetworkPolicyEgressRule), serialize_when_none=False)
    ingress = ListType(ModelType(NetworkPolicyIngressRule), serialize_when_none=False)
    pod_selector = ListType(ModelType(LabelSelector), serialize_when_none=False)
    policy_types = ListType(StringType(), serialize_when_none=False)


class NetworkPolicyStatus(Model):
    conditions = ListType(ModelType(Condition), serialize_when_none=False)


class NetworkPolicy(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(NetworkPolicySpec, serialize_when_none=False)
    status = ModelType(NetworkPolicyStatus, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
