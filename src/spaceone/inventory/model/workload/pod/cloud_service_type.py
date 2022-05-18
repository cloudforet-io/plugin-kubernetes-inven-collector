import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')
count_by_cluster_conf = os.path.join(current_dir, 'widget/count_by_cluster.yml')

cst_pod = CloudServiceTypeResource()
cst_pod.name = 'Pod'
cst_pod.provider = 'kubernetes'
cst_pod.group = 'WorkLoad'
cst_pod.service_code = 'Pod'
cst_pod.is_primary = True
cst_pod.is_major = True
cst_pod.labels = ['Compute', 'Container']
cst_pod.is_primary = True
cst_pod.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/Pod.svg',
}

cst_pod._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Namespace', 'data.namespace'),
        TextDyField.data_source('Pod IP', 'data.status.pod_ip'),
        EnumDyField.data_source('Status', 'data.status.phase', default_state={
            'safe': ['Running', 'Succeeded'],
            'alert': ['Pending', 'Failed', 'Unknown']
        }),
        TextDyField.data_source('Node Name', 'data.node_name'),
        TextDyField.data_source('Host IP', 'data.status.host_ip'),
        DateTimeDyField.data_source('Start Time', 'data.status.start_time'),
        TextDyField.data_source('Uid', 'data.uid', options={
            'is_optional': True
        })
    ],

    search=[
        SearchField.set(name='Uid', key='data.uid'),
        SearchField.set(name='Name', key='name'),
        SearchField.set(name='Namespace', key='data.namespace'),
        SearchField.set(name='Pod IP', key='data.status.pod_ip'),
        SearchField.set(name='Node Name', key='data.node_name'),
        SearchField.set(name='Host IP', key='data.status.host_ip'),
        SearchField.set(name='Start Time', key='data.status.start_time')
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_pod}),
]