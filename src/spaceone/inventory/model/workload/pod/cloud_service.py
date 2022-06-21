from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.workload.pod.data import Pod
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Pod
'''

pod_metadata_base_meta = ItemDynamicLayout.set_fields('Metadata', root_path='data.metadata', fields=[
    TextDyField.data_source('Uid', 'uid'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Namespace', 'namespace'),
    TextDyField.data_source('Cluster Name', 'cluster_name'),
    DateTimeDyField.data_source('Creation Timestamp', 'creation_timestamp'),
    TextDyField.data_source('Deletion grace Period Seconds', 'deletion_grace_period_seconds'),
    DateTimeDyField.data_source('Deletion Timestamp', 'deletion_timestamp'),
    TextDyField.data_source('Finalizers', 'finalizers'),
    TextDyField.data_source('Generate Name', 'generate_name'),
    TextDyField.data_source('Generation', 'generation')
])

pod_metadata_annotations_meta = SimpleTableDynamicLayout.set_fields('Annotations', root_path='data.metadata.annotations', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

pod_metadata_labels_meta = SimpleTableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

pod_metadata_meta = ListDynamicLayout.set_layouts('Metadata', layouts=[pod_metadata_base_meta,
                                                                       pod_metadata_annotations_meta,
                                                                       pod_metadata_labels_meta])
'''
Spec
'''

pod_spec_base_meta = ItemDynamicLayout.set_fields('Spec', root_path='data.spec', fields=[
    TextDyField.data_source('Active Deadline Seconds', 'active_deadline_seconds'),
    TextDyField.data_source('Automount Service Account Token', 'automount_service_account_token'),
    TextDyField.data_source('Enable Service Links', 'enable_service_links'),
    ListDyField.data_source('Host Aliases', 'host_aliases'),
    EnumDyField.data_source('Host Ipc', 'host_ipc', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Host Network', 'host_network', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Host Pid', 'host_pid', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Hostname', 'hostname'),
    TextDyField.data_source('Image Pull Secrets', 'image_pull_secrets'),
    TextDyField.data_source('Node Name', 'node_name'),
    TextDyField.data_source('Preemption Policy', 'preemption_policy'),
    TextDyField.data_source('Priority', 'priority'),
    TextDyField.data_source('Priority Class Name', 'priority_class_name'),
    ListDyField.data_source('Readiness Gates', 'readiness_gates'),
    TextDyField.data_source('Restart Policy', 'restart_policy'),
    TextDyField.data_source('Runtime Class Name', 'runtime_class_name'),
    TextDyField.data_source('Scheduler Name', 'scheduler_name'),
    TextDyField.data_source('Service Account', 'service_account'),
    TextDyField.data_source('Service Account Name', 'service_account_name'),
    EnumDyField.data_source('Set Hostname As FQDN', 'set_hostname_as_fqdn', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Share Process Namespace', 'share_process_namespace', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Subdomain', 'subdomain'),
    TextDyField.data_source('Termination Grace Period Seconds', 'termination_grace_period_seconds'),
    ListDyField.data_source('Tolerations', 'tolerations')
])

pod_spec_node_selector_meta = SimpleTableDynamicLayout.set_fields('Node Selector', root_path='data.spec.node_selector', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

pod_spec_dns_meta = ItemDynamicLayout.set_fields('DNS Config', root_path='data.spec', fields=[
    TextDyField.data_source('DNS Policy', 'dns_policy'),
    ListDyField.data_source('Nameservers', 'dns_config.nameservers'),
    ListDyField.data_source('Searches', 'dns_config.searches'),
    ListDyField.data_source('Options', 'dns_config.options')
])

pod_spec_meta = ListDynamicLayout.set_layouts('Spec', layouts=[pod_spec_base_meta,
                                                               pod_spec_dns_meta,
                                                               pod_spec_node_selector_meta])


'''
Containers
'''

pod_container_base_meta = SimpleTableDynamicLayout.set_fields('Containers', root_path='data.spec.containers', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Ports', 'ports'),
    TextDyField.data_source('Args', 'args'),
    ListDyField.data_source('Command', 'command'),
    ListDyField.data_source('Env', 'env'),
    TextDyField.data_source('Env From', 'env_from'),
    TextDyField.data_source('Image', 'image'),
    TextDyField.data_source('Image Pull Policy', 'image_pull_policy'),
    TextDyField.data_source('Life Cycle', 'lifecycle'),
    TextDyField.data_source('Liveness Probe', 'liveness_probe'),
    TextDyField.data_source('Readiness Probe', 'readiness_probe'),
    TextDyField.data_source('Resource Limits', 'resource'),
    TextDyField.data_source('Security Context', 'security_context'),
    TextDyField.data_source('Startup Probe', 'startup_probe'),
    TextDyField.data_source('Volume Devices', 'volume_devices'),
    ListDyField.data_source('Volume Mounts', 'volume_mounts'),
    TextDyField.data_source('Working Dir', 'working_dir')
])

pod_container_base_init_meta = SimpleTableDynamicLayout.set_fields('Init Containers', root_path='data.spec.init_containers', fields=[
   TextDyField.data_source('Name', 'name'),
   TextDyField.data_source('Ports', 'ports'),
   TextDyField.data_source('Args', 'args'),
   ListDyField.data_source('Command', 'command'),
   ListDyField.data_source('Env', 'env'),
   TextDyField.data_source('Env From', 'env_from'),
   TextDyField.data_source('Image', 'image'),
   TextDyField.data_source('Image Pull Policy', 'image_pull_policy'),
   TextDyField.data_source('Life Cycle', 'lifecycle'),
   TextDyField.data_source('Liveness Probe', 'liveness_probe'),
   TextDyField.data_source('Readiness Probe', 'readiness_probe'),
   TextDyField.data_source('Resource Limits', 'resource'),
   TextDyField.data_source('Security Context', 'security_context'),
   TextDyField.data_source('Startup Probe', 'startup_probe'),
   TextDyField.data_source('Volume Devices', 'volume_devices'),
   ListDyField.data_source('Volume Mounts', 'volume_mounts'),
   TextDyField.data_source('Working Dir', 'working_dir')
])

pod_container_meta = ListDynamicLayout.set_layouts('Containers', layouts=[pod_container_base_meta,
                                                                          pod_container_base_init_meta])

'''
Volumes
'''

pod_volume_meta = ItemDynamicLayout.set_fields('Volumes', root_path='data.spec.volumes', fields=[

])

'''
Status
'''
pod_status_base_meta = ItemDynamicLayout.set_fields('Status', root_path='data.status', fields=[
    TextDyField.data_source('Host IP', 'host_ip'),
    TextDyField.data_source('POD IP', 'pod_ip'),
    ListDyField.data_source('POD IPs', 'pod_i_ps'),
    TextDyField.data_source('QOS Class', 'qos_class'),
    TextDyField.data_source('Message', 'message'),
    TextDyField.data_source('Reason', 'reason'),
    TextDyField.data_source('Nominated Node Name', 'nominated_node_name'),
    TextDyField.data_source('Phase', 'phase'),
    DateTimeDyField.data_source('Start Time', 'start_time')
])

pod_status_conditions_meta = SimpleTableDynamicLayout.set_fields('Conditions', root_path='data.status.conditions', fields=[
    TextDyField.data_source('Type', 'type'),
    TextDyField.data_source('Status', 'status'),
    TextDyField.data_source('Message', 'message'),
    TextDyField.data_source('Reason', 'reason'),
    DateTimeDyField.data_source('Last Probe Time', 'last_probe_time'),
    DateTimeDyField.data_source('Last Transition Time', 'last_transition_time')
])

pod_status_container_status_meta = SimpleTableDynamicLayout.set_fields('Container Statuses', root_path='data.status.container_statuses', fields=[
   TextDyField.data_source('Name', 'name'),
   EnumDyField.data_source('Ready', 'ready', default_badge={
       'indigo.500': ['true'], 'coral.600': ['false']
   }),
   TextDyField.data_source('Restart Count', 'restart_count'),
   EnumDyField.data_source('Started', 'started', default_badge={
       'indigo.500': ['true'], 'coral.600': ['false']
   }),
   TextDyField.data_source('State', 'state'),
   TextDyField.data_source('Container ID', 'container_id'),
   TextDyField.data_source('Image', 'image'),
   TextDyField.data_source('Image Id', 'image_id'),
   TextDyField.data_source('Last State', 'last_state')
])

pod_status_meta = ListDynamicLayout.set_layouts('Status', layouts=[pod_status_container_status_meta,
                                                                   pod_status_conditions_meta,
                                                                   pod_status_container_status_meta])

annotations = TableDynamicLayout.set_fields('Annotations', root_path='data.metadata.annotations', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.metadata.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

pod_meta = CloudServiceMeta.set_layouts([pod_metadata_meta, annotations, labels, pod_spec_meta, pod_container_meta,
                                         pod_volume_meta, pod_status_meta])


class WorkLoadResource(CloudServiceResource):
    cloud_service_group = StringType(default='WorkLoad')


class PodResource(WorkLoadResource):
    cloud_service_type = StringType(default='Pod')
    data = ModelType(Pod)
    _metadata = ModelType(CloudServiceMeta, default=pod_meta, serialized_name='metadata')


class PodResponse(CloudServiceResponse):
    resource = PolyModelType(PodResource)