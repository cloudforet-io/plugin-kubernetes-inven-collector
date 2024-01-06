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
    Labels,
    LoadBalancerStatus,
    Condition,
)


class ClientIPConfig(Model):
    timeout_seconds = IntType(serialize_when_none=False)


class SessionAffinityConfig(Model):
    client_ip = ModelType(ClientIPConfig, serialize_when_none=False)


class ServicePort(Model):
    app_protocol = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    node_port = IntType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    protocol = StringType(choices=("TCP", "UDP", "SCTP"), serialize_when_none=False)
    target_port = StringType(serialize_when_none=False)


class ServiceSpec(Model):
    allocate_loadBalancer_node_ports = BooleanType(serialize_when_none=False)
    cluster_ip = StringType(serialize_when_none=False)
    cluster_ips = ListType(StringType(), serialize_when_none=False)
    external_ips = ListType(StringType(), serialize_when_none=False)
    external_name = StringType(serialize_when_none=False)
    external_traffic_policy = StringType(serialize_when_none=False)
    health_check_node_port = IntType(serialize_when_none=False)
    internal_traffic_policy = StringType(serialize_when_none=False)
    ip_families = ListType(StringType(serialize_when_none=False))
    ip_family_policy = StringType(serialize_when_none=False)
    load_balancer_class = StringType(serialize_when_none=False)
    load_balancer_ip = StringType(serialize_when_none=False)
    load_balancer_source_ranges = ListType(StringType(), serialize_when_none=False)
    ports = ListType(ModelType(ServicePort), serialize_when_none=False)
    publish_not_ready_addresses = BooleanType(serialize_when_none=False)
    selector = ListType(ModelType(Labels), serialize_when_none=False)
    session_affinity = StringType(serialize_when_none=False)
    session_affinity_config = ModelType(
        SessionAffinityConfig, serialize_when_none=False
    )
    type = StringType(
        choices=("ExternalName", "ClusterIP", "NodePort", "LoadBalancer"),
        serialize_when_none=False,
    )


class ServiceStatus(Model):
    conditions = ListType(ModelType(Condition), serialize_when_none=False)
    load_balancer = ModelType(LoadBalancerStatus, serialize_when_none=False)


class Service(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(ServiceSpec, serialize_when_none=False)
    status = ModelType(ServiceStatus, serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
