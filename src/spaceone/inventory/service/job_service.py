import time
import logging
import json
import concurrent.futures

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.core.service import *
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class JobService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(["secret_data", "options"])
    def get_tasks(self, params):
        execute_managers = self._cloud_service_groups_to_types(CLOUD_SERVICE_GROUP_MAP.keys())
        return {'tasks': [{'task_options': {'manager': _manager}} for _manager in execute_managers]}

    @staticmethod
    def _cloud_service_groups_to_types(cloud_service_groups) -> list:
        cloud_service_types = []
        for cloud_service_group in cloud_service_groups:
            if cloud_service_group in CLOUD_SERVICE_GROUP_MAP:
                cloud_service_types.extend(CLOUD_SERVICE_GROUP_MAP[cloud_service_group])

        return cloud_service_types
