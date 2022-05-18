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

cst_daemon_set = CloudServiceTypeResource()
cst_daemon_set.name = 'DaemonSet'
cst_daemon_set.provider = 'kubernetes'
cst_daemon_set.group = 'WorkLoad'
cst_daemon_set.service_code = 'DaemonSet'
cst_daemon_set.is_primary = True
cst_daemon_set.is_major = False
cst_daemon_set.labels = ['Container']
cst_daemon_set.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/daemonset.svg',
}

cst_daemon_set._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Namespace', 'data.metadata.namespace'),
        TextDyField.data_source('Number Ready', 'data.status.number_ready'),
        DateTimeDyField.data_source('Start Time', 'data.metadata.creation_timestamp'),
        TextDyField.data_source('Update Strategy', 'data.spec.update_strategy.type'),
        TextDyField.data_source('Uid', 'data.uid', options={
            'is_optional': True
        })
    ],

    search=[
        SearchField.set(name='Uid', key='data.uid'),
        SearchField.set(name='Name', key='name'),
        SearchField.set(name='Namespace', key='data.metadata.namespace'),
        SearchField.set(name='Number Ready', key='data.status.number_ready'),
        SearchField.set(name='Start Time', key='data.metadata.creation_timestamp'),
        SearchField.set(name='Update Strategy', key='data.spec.update_strategy.type')
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_daemon_set}),
]