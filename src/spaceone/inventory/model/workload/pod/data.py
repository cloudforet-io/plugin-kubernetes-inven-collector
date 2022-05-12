from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType


# Developer defined model
class Labels(Model):
    key = StringType()
    value = StringType()


class ResourceLimits(Model):
    limits = StringType()
    readiness_probe = StringType()


class Capabilities(Model):
    add = ListType(StringType())
    drop = ListType(StringType())


class SELinuxOptions(Model):
    level = StringType()
    role = StringType()
    type = StringType()
    user = StringType()


class SeccompProfile(Model):
    localhost_profile = StringType()
    type = StringType()


class WindowsSecurityContextOptions(Model):
    gmsa_credential_spec = StringType()
    gmsa_credential_spec_name = StringType()
    host_process = BooleanType()
    run_as_user_name = StringType()


class SecurityContext(Model):
    allow_privilege_escalation = BooleanType()
    capabilities = ModelType(Capabilities)
    privileged = BooleanType()
    proc_mount = StringType()
    read_only_root_filesystem = BooleanType()
    run_as_group = IntType()
    run_as_non_root = BooleanType()
    run_as_user = IntType()
    se_linux_options = ModelType(SELinuxOptions)
    seccomp_profile = ModelType(SeccompProfile)
    windows_options = ModelType(WindowsSecurityContextOptions)


class VolumeMount(Model):
    mount_path = StringType()
    mount_propagation = StringType()
    name = StringType()
    read_only = BooleanType()
    sub_path = StringType()
    sub_path_expr = StringType()


class ContainerEnvironment(Model):
    name = StringType()
    value = StringType()


class ContainerPort(Model):
    container_port = IntType()
    host_ip = StringType()
    host_port = IntType()
    name = StringType()
    protocol = StringType()


class ExecAction(Model):
    command = ListType(StringType())


class GRPCAction(Model):
    port = IntType()
    service = StringType()


class HTTPHeader(Model):
    name = StringType()
    value = StringType()


class HTTPGetAction(Model):
    host = StringType()
    http_headers = ListType(ModelType(HTTPHeader))
    path = StringType()
    port = IntType()
    scheme = StringType()


class TCPSocketAction(Model):
    host = StringType()
    port = IntType()


class Probe(Model):
    _exec = ModelType(ExecAction)
    failure_threshold = IntType()
    grpc = ModelType(GRPCAction)
    http_get = ModelType(HTTPHeader)
    initial_delay_seconds = IntType()
    period_seconds = IntType()
    success_threshold = IntType()
    tcp_socket = ModelType(TCPSocketAction)
    termination_grace_period_seconds = IntType()
    timeout_seconds = IntType()


class Container(Model):
    args = ListType(StringType())
    command = ListType(StringType())
    env = ListType(ModelType(ContainerEnvironment))
    env_from = StringType()
    image = StringType()
    image_pull_policy = StringType()
    lifecycle = StringType()
    liveness_probe = ModelType(Probe)
    name = StringType()
    ports = ListType(ModelType(ContainerPort))
    readiness_probe = ModelType(Probe)
    resource = ModelType(ResourceLimits)
    security_context = ModelType(SecurityContext)
    startup_probe = StringType()
    stdin = StringType()
    stdin_once = StringType()
    termination_message_path = StringType()
    termination_message_policy = StringType()
    tty = StringType()
    volume_devices = StringType()
    volume_mounts = ListType(ModelType(VolumeMount))
    working_dir = StringType()


# Developer defined model
class Annotations(Model):
    key = StringType()
    value = StringType()


class ObjectMeta(Model):
    annotations = ListType(ModelType(Annotations), serialize_when_none=False)
    cluster_name = StringType(serialize_when_none=False)
    creation_timestamp = DateTimeType(serialize_when_none=False)
    deletion_grace_period_seconds = StringType(serialize_when_none=False)
    deletion_timestamp = DateTimeType(serialize_when_none=False)
    finalizers = StringType(serialize_when_none=False)
    generate_name = StringType(serialize_when_none=False)
    generation = StringType(serialize_when_none=False)
    labels = ListType(ModelType(Labels), serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)


class NodeSelectorRequirement(Model):
    key = StringType(),
    operator = StringType(),
    values = ListType(StringType())


class NodeSelectorTerm(Model):
    matchExpressions = ListType(ModelType(NodeSelectorRequirement))
    matchFields = ListType(ModelType(NodeSelectorRequirement))


class NodeSelector(Model):
    node_selector_terms = ListType(ModelType(NodeSelectorTerm))


class PreferredSchedulingTerm(Model):
    preference = ModelType(NodeSelectorTerm)
    weight = IntType()


class NodeAffinity(Model):
    preferred_during_scheduling_ignored_during_execution = ListType(ModelType(PreferredSchedulingTerm))
    required_during_scheduling_ignored_during_execution = ModelType(NodeSelector)


# Developer defined model
class MatchLabel(Model):
    key = StringType()
    value = StringType()


class LabelSelectorRequirement(Model):
    key = StringType()
    operator = StringType()
    values = ListType(StringType())


class LabelSelector(Model):
    match_expressions = ListType(ModelType(LabelSelectorRequirement))
    #match_labels = ListType(ModelType(MatchLabel))


class PodAffinityTerm(Model):
    label_selector = ModelType(LabelSelector)
    namespace_selector = ModelType(LabelSelector)
    namespaces = ListType(StringType())
    topology_key = StringType()


class WeightedPodAffinityTerm(Model):
    pod_affinity_term = ModelType(PodAffinityTerm)
    weight = IntType()


class PodAffinity(Model):
    preferred_during_scheduling_ignored_during_execution = ListType(ModelType(WeightedPodAffinityTerm))
    required_during_scheduling_ignored_during_execution = ListType(ModelType(PodAffinityTerm))


class PodAntiAffinity(Model):
    preferred_during_scheduling_ignored_during_execution = ListType(ModelType(WeightedPodAffinityTerm))
    required_during_scheduling_ignored_during_execution = ListType(ModelType(PodAffinityTerm))


class Affinity(Model):
    node_affinity = ModelType(NodeAffinity)
    pod_affinity = ModelType(PodAffinity)
    pod_anti_affinity = ModelType(PodAntiAffinity)


class PodDNSConfigOption(Model):
    name = StringType()
    value = StringType()


class PodDNSConfig(Model):
    nameservers = ListType(StringType())
    options = ListType(ModelType(PodDNSConfigOption))
    searches = ListType(StringType)


class ConfigMapKeySelector(Model):
    key = StringType()
    name = StringType()
    optional = BooleanType()


class ObjectFieldSelector(Model):
    api_version = StringType()
    field_path = StringType()


class ResourceFieldSelector(Model):
    container_name = StringType()
    resource = StringType()


class SecretKeySelector(Model):
    key = StringType()
    name = StringType()
    optional = BooleanType()


class EnvVarSource(Model):
    config_map_key_ref = ModelType(ConfigMapKeySelector)
    field_ref = ModelType(ObjectFieldSelector)
    resource_field_ref = ModelType(ResourceFieldSelector)
    secret_key_ref = ModelType(SecretKeySelector)


class EnvVar(Model):
    name = StringType()
    value = StringType()
    value_from = ModelType(EnvVarSource)


class VolumeDevice(Model):
    device_path = StringType()
    name = StringType()


class EphemeralContainer(Model):
    args = ListType(StringType())
    command = ListType(StringType())
    env = ListType(ModelType(EnvVar))
    image = StringType()
    image_pull_policy = StringType()
    name = StringType()
    security_context = ModelType(SecurityContext)
    stdin = StringType()
    stdin_once = BooleanType()
    target_container_name = StringType()
    termination_message_path = StringType()
    termination_message_policy = StringType()
    tty = BooleanType()
    volume_devices = ListType(ModelType(VolumeDevice))
    volume_mounts = ListType(ModelType(VolumeMount))
    working_dir = StringType()


class HostAlias(Model):
    hostnames = ListType(StringType())
    ip = StringType()


class LocalObjectReference(Model):
    name = StringType()


class PodOS(Model):
    name = StringType()


class PodReadinessGate(Model):
    condition_type = StringType()


class SELinuxOptions(Model):
    level = StringType()
    role = StringType()
    type = StringType()
    user = StringType()


class SeccompProfile(Model):
    localhost_profile = StringType()
    type = StringType()


class Sysctl(Model):
    name = StringType()
    value = StringType()


class WindowsSecurityContextOptions(Model):
    gmsa_credential_spec = StringType()
    gmsa_credential_spec_name = StringType()
    host_process = BooleanType()
    run_as_user_name = StringType()


class PodSecurityContext(Model):
    fs_group = IntType()
    fs_group_change_policy = StringType()
    run_as_group = IntType()
    run_as_non_root = BooleanType()
    run_as_user = IntType()
    se_linux_options = ModelType(SELinuxOptions)
    seccomp_profile = ModelType(SeccompProfile)
    supplemental_groups = ListType(IntType())
    sysctls = ListType(ModelType(Sysctl))
    windows_options = ModelType(WindowsSecurityContextOptions)


class Toleration(Model):
    effect = StringType()
    key = StringType()
    operator = StringType()
    toleration_seconds = IntType()
    value = StringType()


class AWSElasticBlockStoreVolumeSource(Model):
    fs_type = StringType()
    partition = IntType()
    read_only = BooleanType()
    volume_id = StringType()


class AzureDiskVolumeSource(Model):
    caching_mode = StringType()
    disk_name = StringType()
    disk_uri = StringType()
    fs_type = StringType()
    kind = StringType()
    read_only = BooleanType()


class AzureFileVolumeSource(Model):
    read_only = BooleanType()
    secret_name = StringType()
    share_name = StringType()


class CephFSVolumeSource(Model):
    monitors = ListType(StringType())
    path = StringType()
    read_only = BooleanType()
    secret_file = StringType()
    secret_ref = ModelType(LocalObjectReference)
    user = StringType()


class CinderVolumeSource(Model):
    fs_type = StringType()
    read_only = BooleanType()
    secret_ref = ModelType(LocalObjectReference)
    volume_id = StringType()


class KeyToPath(Model):
    key = StringType()
    mode = IntType()
    path = StringType()


class ConfigMapVolumeSource(Model):
    default_mode = IntType()
    items = ListType(ModelType(KeyToPath))
    name = StringType()
    optional = BooleanType()


class CSIVolumeSource(Model):
    driver = StringType()
    fs_type = StringType()
    node_publish_secret_ref = ModelType(LocalObjectReference)
    read_only = BooleanType()


class DownwardAPIVolumeFile(Model):
    field_ref = ModelType(ObjectFieldSelector)
    mode = IntType()
    path = StringType()
    resource_field_ref = ModelType(ResourceFieldSelector)


class DownwardAPIVolumeSource(Model):
    default_mode = IntType()
    items = ListType(ModelType(DownwardAPIVolumeFile))


class EmptyDirVolumeSource(Model):
    medium = StringType()


class TypedLocalObjectReference(Model):
    api_group = StringType()
    kind = StringType()
    name = StringType()


# Custom defined model
class PodLimits(Model):
    cpu = StringType()
    memory = StringType()


class ResourceRequirements(Model):
    limits = ModelType(PodLimits)
    requests = ModelType(PodLimits)


class PersistentVolumeClaimSpec(Model):
    access_modes = ListType(StringType())
    data_source = ModelType(TypedLocalObjectReference)
    data_source_ref = ModelType(TypedLocalObjectReference)
    resources = ModelType(ResourceRequirements)
    selector = ModelType(LabelSelector)
    storage_class_name = StringType()
    volume_mode = StringType()
    volume_name = StringType()


class PersistentVolumeClaimTemplate(Model):
    metadata = ModelType(ObjectMeta)
    spec = ModelType(PersistentVolumeClaimSpec)


class EphemeralVolumeSource(Model):
    volume_claim_template = ModelType(PersistentVolumeClaimTemplate)


class FlexVolumeSource(Model):
    driver = StringType()
    fs_type = StringType()
    read_only = BooleanType()
    secret_ref = ModelType(LocalObjectReference)


class GCEPersistentDiskVolumeSource(Model):
    fs_type = StringType()
    partition = IntType()
    pd_name = StringType()
    read_only = BooleanType()


class GitRepoVolumeSource(Model):
    directory = StringType()
    repository = StringType()
    revision = StringType()


class HostPathVolumeSource(Model):
    path = StringType()
    type = StringType()


class NFSVolumeSource(Model):
    path = StringType()
    read_only = BooleanType()
    server = StringType()


class PersistentVolumeClaimVolumeSource(Model):
    claim_name = StringType()
    read_only = BooleanType()


class SecretVolumeSource(Model):
    default_mode = IntType()
    items = ListType(ModelType(KeyToPath))
    optional = BooleanType()
    secret_name = StringType()


class VsphereVirtualDiskVolumeSource(Model):
    fs_type = StringType()
    storage_policy_id = StringType()
    storage_policy_name = StringType()
    volume_path = StringType()


class Volume(Model):
    name = StringType()
    aws_elastic_block_store = ModelType(AWSElasticBlockStoreVolumeSource)
    azure_disk = ModelType(AzureDiskVolumeSource)
    azure_file = ModelType(AzureFileVolumeSource)
    cephfs = ModelType(CephFSVolumeSource)
    cinder = ModelType(CinderVolumeSource)
    config_map = ModelType(ConfigMapVolumeSource)
    csi = ModelType(CSIVolumeSource)
    downward_api = ModelType(DownwardAPIVolumeSource)
    empty_dir = ModelType(EmptyDirVolumeSource)
    ephemeral = ModelType(EphemeralVolumeSource)
    flex_volume = ModelType(FlexVolumeSource)
    gce_persistent_disk = ModelType(GCEPersistentDiskVolumeSource)
    git_repo = ModelType(GitRepoVolumeSource)
    host_path = ModelType(HostPathVolumeSource)
    nfs = ModelType(NFSVolumeSource)
    persistent_volume_claim = ModelType(PersistentVolumeClaimVolumeSource)
    secret = ModelType(SecretVolumeSource)
    vsphere_volume = ModelType(VsphereVirtualDiskVolumeSource)


class PodSpec(Model):
    active_deadline_seconds = StringType()
    affinity = ModelType(Affinity)
    automount_service_account_token = BooleanType()
    containers = ListType(ModelType(Container))
    dns_config = ModelType(PodDNSConfig)
    dns_policy = StringType()
    enable_service_links = BooleanType()
    ephemeral_containers = ModelType(EphemeralContainer)
    host_aliases = ListType(ModelType(HostAlias))
    host_ipc = BooleanType()
    host_network = BooleanType()
    host_pid = BooleanType()
    hostname = StringType()
    image_pull_secrets = ModelType(LocalObjectReference)
    init_containers = ListType(ModelType(Container))
    node_name = StringType()
    node_selector = ListType(ModelType(Labels))
    os = ModelType(PodOS)
    preemption_policy = StringType()
    priority = IntType()
    priority_class_name = StringType()
    readiness_gates = ListType(ModelType(PodReadinessGate))
    restart_policy = StringType()
    runtime_class_name = StringType()
    scheduler_name = StringType()
    security_context = ModelType(PodSecurityContext)
    service_account = StringType()
    service_account_name = StringType()
    set_hostname_as_fqdn = BooleanType()
    share_process_namespace = BooleanType()
    subdomain = StringType()
    termination_grace_period_seconds = IntType()
    tolerations = ListType(ModelType(Toleration))
    volumes = ListType(ModelType(Volume))


class PodCondition(Model):
    last_probe_time = DateTimeType()
    last_transition_time = DateTimeType()
    message = StringType()
    reason = StringType()
    status = StringType()
    type = StringType()


class ContainerStateRunning(Model):
    started_at = DateTimeType()


class ContainerStateTerminated(Model):
    container_id = StringType()
    exit_code = IntType()
    finished_at = DateTimeType()
    message = StringType()
    reason = StringType()
    signal = IntType()
    started_at = DateTimeType()


class ContainerStateWaiting(Model):
    message = StringType()
    reason = StringType()


class ContainerState(Model):
    running = ModelType(ContainerStateRunning)
    terminated = ModelType(ContainerStateTerminated)
    waiting = ModelType(ContainerStateWaiting)


class ContainerStatus(Model):
    container_id = StringType()
    image = StringType()
    image_id = StringType()
    last_state = ModelType(ContainerState)
    name = StringType()
    ready = BooleanType()
    restart_count = IntType()
    started = BooleanType()
    state = ModelType(ContainerState)


class PodIP(Model):
    ip = StringType()


class PodStatus(Model):
    conditions = ListType(ModelType(PodCondition))
    container_statuses = ListType(ModelType(ContainerStatus))
    ephemeral_container_statuses = ListType(ModelType(ContainerStatus))
    init_container_statuses = ListType(ModelType(ContainerStatus))
    host_ip = StringType()
    message = StringType()
    nominated_node_name = StringType()
    phase = StringType()
    pod_ip = StringType()
    pod_i_ps = ListType(ModelType(PodIP))
    qos_class = StringType()
    reason = StringType()
    start_time = DateTimeType()


class Pod(Model):
    api_version = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(PodSpec, serialize_when_none=False)
    status = ModelType(PodStatus, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": '',
            "external_link": f""
        }
