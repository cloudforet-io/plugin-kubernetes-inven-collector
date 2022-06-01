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

cst_role = CloudServiceTypeResource()
cst_role.name = 'Role'
cst_role.provider = 'kubernetes'
cst_role.group = 'Authorization'
cst_role.service_code = 'Role'
cst_role.is_primary = True
cst_role.is_major = True
cst_role.labels = ['Security', 'Management']
cst_role.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/role.svg',
}

cst_role._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('CPU', 'data.status.capacity.cpu'),
        SizeField.data_source('Memory', 'data.status.capacity.memory'),
        DateTimeDyField.data_source('Start Time', 'data.metadata.creation_timestamp'),
        TextDyField.data_source('Update Strategy', 'data.spec.update_strategy.type'),
        TextDyField.data_source('Uid', 'data.uid', options={
            'is_optional': True
        })
    ],

    search=[
        SearchField.set(name='Uid', key='data.uid'),
        SearchField.set(name='Name', key='name'),
        SearchField.set(name='CPU', key='data.status.capacity.cpu'),
        SearchField.set(name='Memory', key='data.status.capacity.memory'),
        SearchField.set(name='Start Time', key='data.metadata.creation_timestamp')
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_role}),
]
