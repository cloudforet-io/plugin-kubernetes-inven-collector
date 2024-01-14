from schematics import Model
from schematics.types import (
    ListType,
    StringType,
    PolyModelType,
    DictType,
    ModelType,
    DateTimeType,
    BooleanType,
    IntType,
)

from spaceone.inventory.libs.schema.metadata.dynamic_layout import BaseLayoutField
from spaceone.inventory.libs.schema.metadata.dynamic_search import BaseDynamicSearch
from spaceone.inventory.libs.schema.metadata.dynamic_widget import BaseDynamicWidget


class MetaDataViewSubData(Model):
    layouts = ListType(PolyModelType(BaseLayoutField))


class MetaDataViewTable(Model):
    layout = PolyModelType(BaseLayoutField)


class MetaDataView(Model):
    table = PolyModelType(MetaDataViewTable, serialize_when_none=False)
    sub_data = PolyModelType(MetaDataViewSubData, serialize_when_none=False)
    search = ListType(PolyModelType(BaseDynamicSearch), serialize_when_none=False)
    widget = ListType(PolyModelType(BaseDynamicWidget), serialize_when_none=False)


class BaseMetaData(Model):
    view = ModelType(MetaDataView)


class BaseResponse(Model):
    state = StringType(default="SUCCESS", choices=("SUCCESS", "FAILURE", "TIMEOUT"))
    message = StringType(default="")
    resource_type = StringType(required=True)
    match_rules = DictType(ListType(StringType), serialize_when_none=False)
    resource = PolyModelType(Model, default={})


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


"""
Model Data
"""


# Developer defined model
class Annotations(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class Labels(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


# Developer defined model
class MatchLabel(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class LabelSelectorRequirement(Model):
    key = StringType(serialize_when_none=False)
    operator = StringType(serialize_when_none=False)
    values = ListType(StringType(), serialize_when_none=False)


class LabelSelector(Model):
    match_expressions = ListType(
        ModelType(LabelSelectorRequirement), serialize_when_none=False
    )
    match_labels = ListType(ModelType(MatchLabel))


class OwnerReference(Model):
    block_owner_deletion = BooleanType(serialize_when_none=False)
    controller = BooleanType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)


class ObjectMeta(Model):
    annotations = ListType(ModelType(Annotations), serialize_when_none=False)
    creation_timestamp = DateTimeType(serialize_when_none=False)
    deletion_grace_period_seconds = StringType(serialize_when_none=False)
    deletion_timestamp = DateTimeType(serialize_when_none=False)
    finalizers = ListType(StringType(), serialize_when_none=False)
    generate_name = StringType(serialize_when_none=False)
    generation = StringType(serialize_when_none=False)
    labels = ListType(ModelType(Labels), serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    owner_references = ListType(ModelType(OwnerReference), serialize_when_none=False)


class ListMeta(Model):
    _continue = StringType(serialize_when_none=False)
    remaining_item_count = IntType(serialize_when_none=False)
    resource_version = StringType(serialize_when_none=False)
    self_link = StringType(serialize_when_none=False)


class PodAffinityTerm(Model):
    label_selector = ModelType(LabelSelector, serialize_when_none=False)
    namespace_selector = ModelType(LabelSelector, serialize_when_none=False)
    namespaces = ListType(StringType(), serialize_when_none=False)
    topology_key = StringType(serialize_when_none=False)


class WeightedPodAffinityTerm(Model):
    pod_affinity_term = ModelType(PodAffinityTerm, serialize_when_none=False)
    weight = IntType(serialize_when_none=False)


class PodAffinity(Model):
    preferred_during_scheduling_ignored_during_execution = ListType(
        ModelType(WeightedPodAffinityTerm), serialize_when_none=False
    )
    required_during_scheduling_ignored_during_execution = ListType(
        ModelType(PodAffinityTerm), serialize_when_none=False
    )


class PodAntiAffinity(Model):
    preferred_during_scheduling_ignored_during_execution = ListType(
        ModelType(WeightedPodAffinityTerm), serialize_when_none=False
    )
    required_during_scheduling_ignored_during_execution = ListType(
        ModelType(PodAffinityTerm), serialize_when_none=False
    )


class NodeSelectorRequirement(Model):
    key = (StringType(serialize_when_none=False),)
    operator = (StringType(serialize_when_none=False),)
    values = ListType(StringType(), serialize_when_none=False)


class NodeSelectorTerm(Model):
    matchExpressions = ListType(
        ModelType(NodeSelectorRequirement), serialize_when_none=False
    )
    matchFields = ListType(
        ModelType(NodeSelectorRequirement), serialize_when_none=False
    )


class NodeSelector(Model):
    node_selector_terms = ListType(
        ModelType(NodeSelectorTerm), serialize_when_none=False
    )


class PreferredSchedulingTerm(Model):
    preference = ModelType(NodeSelectorTerm, serialize_when_none=False)
    weight = IntType(serialize_when_none=False)


class NodeAffinity(Model):
    preferred_during_scheduling_ignored_during_execution = ListType(
        ModelType(PreferredSchedulingTerm), serialize_when_none=False
    )
    required_during_scheduling_ignored_during_execution = ModelType(
        NodeSelector, serialize_when_none=False
    )


class Affinity(Model):
    node_affinity = ModelType(NodeAffinity, serialize_when_none=False)
    pod_affinity = ModelType(PodAffinity, serialize_when_none=False)
    pod_anti_affinity = ModelType(PodAntiAffinity, serialize_when_none=False)


class WindowsSecurityContextOptions(Model):
    gmsa_credential_spec = StringType(serialize_when_none=False)
    gmsa_credential_spec_name = StringType(serialize_when_none=False)
    host_process = BooleanType(serialize_when_none=False)
    run_as_user_name = StringType(serialize_when_none=False)


class SELinuxOptions(Model):
    level = StringType(serialize_when_none=False)
    role = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    user = StringType(serialize_when_none=False)


class SeccompProfile(Model):
    localhost_profile = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Capabilities(Model):
    add = ListType(StringType(), serialize_when_none=False)
    drop = ListType(StringType(), serialize_when_none=False)


class SecurityContext(Model):
    allow_privilege_escalation = BooleanType(serialize_when_none=False)
    capabilities = ModelType(Capabilities, serialize_when_none=False)
    privileged = BooleanType(serialize_when_none=False)
    proc_mount = StringType(serialize_when_none=False)
    read_only_root_filesystem = BooleanType(serialize_when_none=False)
    run_as_group = IntType(serialize_when_none=False)
    run_as_non_root = BooleanType(serialize_when_none=False)
    run_as_user = IntType(serialize_when_none=False)
    se_linux_options = ModelType(SELinuxOptions, serialize_when_none=False)
    seccomp_profile = ModelType(SeccompProfile, serialize_when_none=False)
    windows_options = ModelType(
        WindowsSecurityContextOptions, serialize_when_none=False
    )


class ExecAction(Model):
    command = ListType(StringType(), serialize_when_none=False)


class GRPCAction(Model):
    port = IntType(serialize_when_none=False)
    service = StringType(serialize_when_none=False)


class HTTPHeader(Model):
    name = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class HTTPGetAction(Model):
    host = StringType(serialize_when_none=False)
    http_headers = ListType(ModelType(HTTPHeader), serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    scheme = StringType(serialize_when_none=False)


class TCPSocketAction(Model):
    host = StringType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)


class Probe(Model):
    _exec = ModelType(ExecAction, serialize_when_none=False)
    failure_threshold = IntType(serialize_when_none=False)
    grpc = ModelType(GRPCAction, serialize_when_none=False)
    http_get = ModelType(HTTPHeader, serialize_when_none=False)
    initial_delay_seconds = IntType(serialize_when_none=False)
    period_seconds = IntType(serialize_when_none=False)
    success_threshold = IntType(serialize_when_none=False)
    tcp_socket = ModelType(TCPSocketAction, serialize_when_none=False)
    termination_grace_period_seconds = IntType(serialize_when_none=False)
    timeout_seconds = IntType(serialize_when_none=False)


class ContainerPort(Model):
    container_port = IntType(serialize_when_none=False)
    host_ip = StringType(serialize_when_none=False)
    host_port = IntType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    protocol = StringType(serialize_when_none=False)


class ContainerEnvironment(Model):
    name = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class ResourceLimits(Model):
    limits = StringType(serialize_when_none=False)
    readiness_probe = StringType(serialize_when_none=False)


class VolumeMount(Model):
    mount_path = StringType(serialize_when_none=False)
    mount_propagation = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    sub_path = StringType(serialize_when_none=False)
    sub_path_expr = StringType(serialize_when_none=False)


class LifecycleHandler(Model):
    exec = (ModelType(ExecAction, serialize_when_none=False),)
    http_get = (ModelType(HTTPGetAction, serialize_when_none=False),)
    tcp_socket = ModelType(TCPSocketAction, serialize_when_none=False)


class ContainerLifeCycle(Model):
    post_start = ModelType(LifecycleHandler, serialize_when_none=False)
    pre_stop = ModelType(LifecycleHandler, serialize_when_none=False)


class Container(Model):
    args = ListType(StringType(), serialize_when_none=False)
    command = ListType(StringType(), serialize_when_none=False)
    env = ListType(ModelType(ContainerEnvironment), serialize_when_none=False)
    env_from = StringType(serialize_when_none=False)
    image = StringType(serialize_when_none=False)
    image_pull_policy = StringType(serialize_when_none=False)
    lifecycle = ModelType(
        ContainerLifeCycle, deserialize_from="lifecycle", serialize_when_none=False
    )
    liveness_probe = ModelType(Probe, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    ports = ListType(ModelType(ContainerPort), serialize_when_none=False)
    readiness_probe = ModelType(Probe, serialize_when_none=False)
    resource = ModelType(ResourceLimits, serialize_when_none=False)
    security_context = ModelType(SecurityContext, serialize_when_none=False)
    startup_probe = ModelType(Probe, serialize_when_none=False)
    stdin = BooleanType(serialize_when_none=False)
    stdin_once = BooleanType(serialize_when_none=False)
    termination_message_path = StringType(serialize_when_none=False)
    termination_message_policy = StringType(serialize_when_none=False)
    tty = BooleanType(serialize_when_none=False)
    volume_devices = StringType(serialize_when_none=False)
    volume_mounts = ListType(ModelType(VolumeMount), serialize_when_none=False)
    working_dir = StringType(serialize_when_none=False)


class PodDNSConfigOption(Model):
    name = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class PodDNSConfig(Model):
    nameservers = ListType(StringType(), serialize_when_none=False)
    options = ListType(ModelType(PodDNSConfigOption), serialize_when_none=False)
    searches = ListType(StringType, serialize_when_none=False)


class ConfigMapKeySelector(Model):
    key = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    optional = BooleanType(serialize_when_none=False)


class ObjectFieldSelector(Model):
    api_version = StringType(serialize_when_none=False)
    field_path = StringType(serialize_when_none=False)


class ResourceFieldSelector(Model):
    container_name = StringType(serialize_when_none=False)
    resource = StringType(serialize_when_none=False)


class SecretKeySelector(Model):
    key = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    optional = BooleanType(serialize_when_none=False)


class EnvVarSource(Model):
    config_map_key_ref = ModelType(ConfigMapKeySelector, serialize_when_none=False)
    field_ref = ModelType(ObjectFieldSelector, serialize_when_none=False)
    resource_field_ref = ModelType(ResourceFieldSelector, serialize_when_none=False)
    secret_key_ref = ModelType(SecretKeySelector, serialize_when_none=False)


class EnvVar(Model):
    name = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)
    value_from = ModelType(EnvVarSource, serialize_when_none=False)


class VolumeDevice(Model):
    device_path = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class EphemeralContainer(Model):
    args = ListType(StringType(), serialize_when_none=False)
    command = ListType(StringType(), serialize_when_none=False)
    env = ListType(ModelType(EnvVar), serialize_when_none=False)
    image = StringType(serialize_when_none=False)
    image_pull_policy = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    security_context = ModelType(SecurityContext, serialize_when_none=False)
    stdin = StringType(serialize_when_none=False)
    stdin_once = BooleanType(serialize_when_none=False)
    target_container_name = StringType(serialize_when_none=False)
    termination_message_path = StringType(serialize_when_none=False)
    termination_message_policy = StringType(serialize_when_none=False)
    tty = BooleanType(serialize_when_none=False)
    volume_devices = ListType(ModelType(VolumeDevice), serialize_when_none=False)
    volume_mounts = ListType(ModelType(VolumeMount), serialize_when_none=False)
    working_dir = StringType(serialize_when_none=False)


class Sysctl(Model):
    name = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class PodSecurityContext(Model):
    fs_group = IntType(serialize_when_none=False)
    fs_group_change_policy = StringType(serialize_when_none=False)
    run_as_group = IntType(serialize_when_none=False)
    run_as_non_root = BooleanType(serialize_when_none=False)
    run_as_user = IntType(serialize_when_none=False)
    se_linux_options = ModelType(SELinuxOptions, serialize_when_none=False)
    seccomp_profile = ModelType(SeccompProfile, serialize_when_none=False)
    supplemental_groups = ListType(IntType(), serialize_when_none=False)
    sysctls = ListType(ModelType(Sysctl), serialize_when_none=False)
    windows_options = ModelType(
        WindowsSecurityContextOptions, serialize_when_none=False
    )


class PodReadinessGate(Model):
    condition_type = StringType(serialize_when_none=False)


class PodOS(Model):
    name = StringType(serialize_when_none=False)


class LocalObjectReference(Model):
    name = StringType(serialize_when_none=False)


class HostAlias(Model):
    hostnames = ListType(StringType())
    ip = StringType(serialize_when_none=False)


class Toleration(Model):
    effect = StringType(serialize_when_none=False)
    key = StringType(serialize_when_none=False)
    operator = StringType(serialize_when_none=False)
    toleration_seconds = IntType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class SecretReference(Model):
    name = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)


class AWSElasticBlockStoreVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    partition = IntType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    volume_id = StringType(serialize_when_none=False)


class AzureDiskVolumeSource(Model):
    caching_mode = StringType(serialize_when_none=False)
    disk_name = StringType(serialize_when_none=False)
    disk_uri = StringType(serialize_when_none=False)
    fs_type = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)


class AzureFileVolumeSource(Model):
    read_only = BooleanType(serialize_when_none=False)
    secret_name = StringType(serialize_when_none=False)
    share_name = StringType(serialize_when_none=False)


class CephFSVolumeSource(Model):
    monitors = ListType(StringType(), serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_file = StringType(serialize_when_none=False)
    secret_ref = ModelType(LocalObjectReference, serialize_when_none=False)
    user = StringType(serialize_when_none=False)


class CinderVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(LocalObjectReference, serialize_when_none=False)
    volume_id = StringType(serialize_when_none=False)


class FCVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    lun = IntType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    target_wwns = ListType(StringType(), serialize_when_none=False)
    wwids = ListType(StringType(), serialize_when_none=False)


class PhotonPersistentDiskVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    pd_id = StringType(serialize_when_none=False)


class PortworxVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    volume_id = StringType(serialize_when_none=False)


class QuobyteVolumeSource(Model):
    group = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    registry = StringType(serialize_when_none=False)
    tenant = StringType(serialize_when_none=False)
    user = StringType(serialize_when_none=False)
    volume = StringType(serialize_when_none=False)


class RBDPersistentVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    image = StringType(serialize_when_none=False)
    keyring = StringType(serialize_when_none=False)
    monitors = ListType(StringType(), serialize_when_none=False)
    pool = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(SecretReference, serialize_when_none=False)
    user = StringType(serialize_when_none=False)


class KeyToPath(Model):
    key = StringType(serialize_when_none=False)
    mode = IntType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)


class ConfigMapVolumeSource(Model):
    default_mode = IntType(serialize_when_none=False)
    items = ListType(ModelType(KeyToPath), serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    optional = BooleanType(serialize_when_none=False)


class CSIVolumeSource(Model):
    driver = StringType(serialize_when_none=False)
    fs_type = StringType(serialize_when_none=False)
    node_publish_secret_ref = ModelType(LocalObjectReference, serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)


class DownwardAPIVolumeFile(Model):
    field_ref = ModelType(ObjectFieldSelector, serialize_when_none=False)
    mode = IntType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    resource_field_ref = ModelType(ResourceFieldSelector, serialize_when_none=False)


class DownwardAPIVolumeSource(Model):
    default_mode = IntType(serialize_when_none=False)
    items = ListType(ModelType(DownwardAPIVolumeFile), serialize_when_none=False)


class EmptyDirVolumeSource(Model):
    medium = StringType(serialize_when_none=False)


class TypedLocalObjectReference(Model):
    api_group = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


# Custom defined model
class PodLimits(Model):
    cpu = StringType(serialize_when_none=False)
    memory = StringType(serialize_when_none=False)


class ResourceRequirements(Model):
    limits = ModelType(PodLimits, serialize_when_none=False)
    requests = ModelType(PodLimits, serialize_when_none=False)


class PersistentVolumeClaimSpec(Model):
    access_modes = ListType(StringType(), serialize_when_none=False)
    data_source = ModelType(TypedLocalObjectReference)
    data_source_ref = ModelType(TypedLocalObjectReference, serialize_when_none=False)
    resources = ModelType(ResourceRequirements, serialize_when_none=False)
    selector = ModelType(LabelSelector, serialize_when_none=False)
    storage_class_name = StringType(serialize_when_none=False)
    volume_mode = StringType(serialize_when_none=False)
    volume_name = StringType(serialize_when_none=False)


class PersistentVolumeClaimTemplate(Model):
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(PersistentVolumeClaimSpec, serialize_when_none=False)


class EphemeralVolumeSource(Model):
    volume_claim_template = ModelType(
        PersistentVolumeClaimTemplate, serialize_when_none=False
    )


class FlexVolumeSource(Model):
    driver = StringType(serialize_when_none=False)
    fs_type = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(LocalObjectReference, serialize_when_none=False)


class GCEPersistentDiskVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    partition = IntType(serialize_when_none=False)
    pd_name = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)


class GitRepoVolumeSource(Model):
    directory = StringType(serialize_when_none=False)
    repository = StringType(serialize_when_none=False)
    revision = StringType(serialize_when_none=False)


class HostPathVolumeSource(Model):
    path = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NFSVolumeSource(Model):
    path = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    server = StringType(serialize_when_none=False)


class PersistentVolumeClaimVolumeSource(Model):
    claim_name = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)


class SecretVolumeSource(Model):
    default_mode = IntType(serialize_when_none=False)
    items = ListType(ModelType(KeyToPath), serialize_when_none=False)
    optional = BooleanType(serialize_when_none=False)
    secret_name = StringType(serialize_when_none=False)


class VsphereVirtualDiskVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    storage_policy_id = StringType(serialize_when_none=False)
    storage_policy_name = StringType(serialize_when_none=False)
    volume_path = StringType(serialize_when_none=False)


class Volume(Model):
    name = StringType(serialize_when_none=False)
    aws_elastic_block_store = ModelType(
        AWSElasticBlockStoreVolumeSource, serialize_when_none=False
    )
    azure_disk = ModelType(AzureDiskVolumeSource, serialize_when_none=False)
    azure_file = ModelType(AzureFileVolumeSource, serialize_when_none=False)
    cephfs = ModelType(CephFSVolumeSource, serialize_when_none=False)
    cinder = ModelType(CinderVolumeSource, serialize_when_none=False)
    config_map = ModelType(ConfigMapVolumeSource, serialize_when_none=False)
    csi = ModelType(CSIVolumeSource, serialize_when_none=False)
    downward_api = ModelType(DownwardAPIVolumeSource, serialize_when_none=False)
    empty_dir = ModelType(EmptyDirVolumeSource, serialize_when_none=False)
    ephemeral = ModelType(EphemeralVolumeSource, serialize_when_none=False)
    flex_volume = ModelType(FlexVolumeSource, serialize_when_none=False)
    gce_persistent_disk = ModelType(
        GCEPersistentDiskVolumeSource, serialize_when_none=False
    )
    git_repo = ModelType(GitRepoVolumeSource, serialize_when_none=False)
    host_path = ModelType(HostPathVolumeSource, serialize_when_none=False)
    nfs = ModelType(NFSVolumeSource, serialize_when_none=False)
    persistent_volume_claim = ModelType(
        PersistentVolumeClaimVolumeSource, serialize_when_none=False
    )
    secret = ModelType(SecretVolumeSource, serialize_when_none=False)
    vsphere_volume = ModelType(
        VsphereVirtualDiskVolumeSource, serialize_when_none=False
    )


class PodSpec(Model):
    active_deadline_seconds = StringType(serialize_when_none=False)
    # affinity = ModelType(Affinity, serialize_when_none=False)
    automount_service_account_token = BooleanType(serialize_when_none=False)
    containers = ListType(ModelType(Container), serialize_when_none=False)
    dns_config = ModelType(PodDNSConfig, serialize_when_none=False)
    dns_policy = StringType(serialize_when_none=False)
    enable_service_links = BooleanType(serialize_when_none=False)
    ephemeral_containers = ModelType(EphemeralContainer, serialize_when_none=False)
    host_aliases = ListType(ModelType(HostAlias), serialize_when_none=False)
    host_ipc = BooleanType(serialize_when_none=False)
    host_network = BooleanType(serialize_when_none=False)
    host_pid = BooleanType(serialize_when_none=False)
    hostname = StringType(serialize_when_none=False)
    image_pull_secrets = ListType(
        ModelType(LocalObjectReference), serialize_when_none=False
    )
    init_containers = ListType(ModelType(Container), serialize_when_none=False)
    node_name = StringType(serialize_when_none=False)
    node_selector = ListType(ModelType(Labels), serialize_when_none=False)
    os = ModelType(PodOS, serialize_when_none=False)
    preemption_policy = StringType(serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    priority_class_name = StringType(serialize_when_none=False)
    readiness_gates = ListType(ModelType(PodReadinessGate), serialize_when_none=False)
    restart_policy = StringType(serialize_when_none=False)
    runtime_class_name = StringType(serialize_when_none=False)
    scheduler_name = StringType(serialize_when_none=False)
    security_context = ModelType(PodSecurityContext, serialize_when_none=False)
    service_account = StringType(serialize_when_none=False)
    service_account_name = StringType(serialize_when_none=False)
    set_hostname_as_fqdn = BooleanType(serialize_when_none=False)
    share_process_namespace = BooleanType(serialize_when_none=False)
    subdomain = StringType(serialize_when_none=False)
    termination_grace_period_seconds = IntType(serialize_when_none=False)
    tolerations = ListType(ModelType(Toleration), serialize_when_none=False)
    volumes = ListType(ModelType(Volume), serialize_when_none=False)


class PodTemplateSpec(Model):
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(PodSpec, serialize_when_none=False)


class PodFailurePolicyOnPodConditionsPattern(Model):
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PodFailurePolicyOnExitCodesRequirement(Model):
    containerName = StringType(serialize_when_none=False)
    operator = StringType(serialize_when_none=False)
    values = ListType(IntType, serialize_when_none=False)


class PodFailurePolicyRule(Model):
    action = StringType(serialize_when_none=False)
    on_exit_codes = ModelType(
        PodFailurePolicyOnExitCodesRequirement, serialize_when_none=False
    )
    on_pod_conditions = ListType(
        ModelType(PodFailurePolicyOnPodConditionsPattern), serialize_when_none=False
    )


class PodFailurePolicy(Model):
    rules = ListType(ModelType(PodFailurePolicyRule), serialize_when_none=False)


class PortStatus(Model):
    error = StringType(serialize_when_none=False)
    port = StringType(serialize_when_none=False)
    protocol = StringType(choices=("TCP", "UDP", "SCTP"), serialize_when_none=False)


class UncountedTerminatedPods(Model):
    failed = ListType(StringType, serialize_when_none=False)
    succeeded = ListType(StringType, serialize_when_none=False)


class LoadBalancerIngress(Model):
    hostname = StringType(serialize_when_none=False)
    ip = StringType(serialize_when_none=False)
    ports = ListType(ModelType(PortStatus), serialize_when_none=False)


class LoadBalancerStatus(Model):
    ingress = ListType(ModelType(LoadBalancerIngress), serialize_when_none=False)


class Condition(Model):
    last_transition_time = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    observed_generation = IntType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ObjectReference(Model):
    api_version = StringType(serialize_when_none=False)
    field_path = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)
    resource_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)


class PolicyRule(Model):
    api_groups = ListType(StringType(), serialize_when_none=False)
    non_resource_urls = ListType(StringType(), serialize_when_none=False)
    resource_names = ListType(StringType(), serialize_when_none=False)
    resources = ListType(StringType(), serialize_when_none=False)
    verbs = ListType(StringType(), serialize_when_none=False)
