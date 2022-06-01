from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.service.network_policy.data import NetworkPolicy
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, ListDyField, DictDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Network Policy
'''

network_policy_meta = CloudServiceMeta.set_layouts([])


class ServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Service')


class NetworkPolicyResource(ServiceResource):
    cloud_service_type = StringType(default='NetworkPolicy')
    data = ModelType(NetworkPolicy)
    _metadata = ModelType(CloudServiceMeta, default=network_policy_meta, serialized_name='metadata')


class NetworkPolicyResponse(CloudServiceResponse):
    resource = PolyModelType(NetworkPolicyResource)
