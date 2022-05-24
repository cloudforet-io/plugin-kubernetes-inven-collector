from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, Labels, LoadBalancerStatus


class TypedLocalObjectReference(Model):
    apiGroup = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class ServiceBackendPort(Model):
    name = StringType(serialize_when_none=False)
    number = IntType(serialize_when_none=False)


class IngressServiceBackend(Model):
    name = StringType(serialize_when_none=False)
    port = ModelType(ServiceBackendPort, serialize_when_none=False)


class IngressBackend(Model):
    resource = ModelType(TypedLocalObjectReference, serialize_when_none=False)
    service = ModelType(IngressServiceBackend, serialize_when_none=False)


class HTTPIngressPath(Model):
    backend = ModelType(IngressBackend, serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    pathType = StringType(serialize_when_none=False)


class HTTPIngressRuleValue(Model):
    paths = ListType(ModelType(HTTPIngressPath), serialize_when_none=False)


class IngressRule(Model):
    host = StringType(serialize_when_none=False)
    http = ModelType(HTTPIngressRuleValue, serialize_when_none=False)


class IngressTLS(Model):
    hosts = ListType(StringType(), serialize_when_none=False)
    secretName = StringType(serialize_when_none=False)


class IngressSpec(Model):
    defaultBackend = ModelType(IngressBackend, serialize_when_none=False)
    ingressClassName = StringType(serialize_when_none=False)
    rules = ListType(ModelType(IngressRule), serialize_when_none=False)
    tls = ListType(ModelType(IngressTLS), serialize_when_none=False)


class IngressStatus(Model):
    loadBalancer = ModelType(LoadBalancerStatus, serialize_when_none=False)


class Ingress(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(IngressSpec, serialize_when_none=False)
    status = ModelType(IngressStatus, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
