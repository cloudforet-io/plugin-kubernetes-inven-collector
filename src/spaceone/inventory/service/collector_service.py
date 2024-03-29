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
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        # set kubernetes service manager
        self.execute_managers = []
        """
        self.execute_managers = [
            'WorkLoad',
        ]
        """

    @check_required(["options"])
    def init(self, params):
        """init plugin by options"""
        capability = {
            "filter_format": FILTER_FORMAT,
            "supported_resource_type": SUPPORTED_RESOURCE_TYPE,
            "supported_features": SUPPORTED_FEATURES,
            "supported_schedules": SUPPORTED_SCHEDULES,
        }
        return {"metadata": capability}

    @transaction
    @check_required(["options", "secret_data"])
    def verify(self, params):
        _LOGGER.debug(f"verify ok")
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params["options"]
        secret_data = params.get("secret_data", {})
        if secret_data != {}:
            kubernetes_manager = KubernetesManager()
            active = kubernetes_manager.verify({}, secret_data)

        return {}

    @transaction
    @check_required(["options", "secret_data", "filter"])
    def collect(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        start_time = time.time()

        _LOGGER.debug(f"EXECUTOR START: Kubernetes Service")
        options = params["options"]

        # Get target manager to collect
        try:
            self.execute_managers = self._get_target_execute_manager(
                params.get("options", {}), params.get('task_options', {})
            )
            _LOGGER.debug(f"[collect] execute_managers => {self.execute_managers}")
        except Exception as e:
            _LOGGER.error(
                f"[collect] failed to get target execute_managers => {e}", exc_info=True
            )
            error_resource_response = self.generate_error_response(
                e, "", "inventory.Error"
            )
            yield error_resource_response.to_primitive()

        # Execute manager
        for execute_manager in self.execute_managers:
            try:
                target_manager = self.locator.get_manager(execute_manager)
                future_executor = target_manager.collect_resources(params)
                for result in future_executor:
                    yield result.to_primitive()
            except Exception as e:
                _LOGGER.error(f"[collect] failed to yield result => {e}", exc_info=True)
                error_resource_response = self.generate_error_response(
                    e, "", "inventory.Error"
                )
                yield error_resource_response.to_primitive()

        _LOGGER.debug(f"TOTAL TIME : {time.time() - start_time} Seconds")

    def _get_target_execute_manager(self, options, task_options):
        if task_options and 'manager' in task_options:
            execute_managers = [task_options['manager']]
        elif "cloud_service_types" in options:
            execute_managers = self._cloud_service_groups_to_types(options["cloud_service_types"])
        else:
            execute_managers = self._cloud_service_groups_to_types(CLOUD_SERVICE_GROUP_MAP.keys())

        return execute_managers

    @staticmethod
    def _cloud_service_groups_to_types(cloud_service_groups) -> list:
        cloud_service_types = []
        for cloud_service_group in cloud_service_groups:
            if cloud_service_group in CLOUD_SERVICE_GROUP_MAP:
                cloud_service_types.extend(CLOUD_SERVICE_GROUP_MAP[cloud_service_group])

        return cloud_service_types

    @staticmethod
    def _match_execute_manager(cloud_service_types):
        target_cloud_service_types = []
        for cloud_service_type in cloud_service_types:
            if cloud_service_type in CLOUD_SERVICE_GROUP_MAP:
                target_cloud_service_types.append(
                    CLOUD_SERVICE_GROUP_MAP[cloud_service_type]
                )

        return target_cloud_service_types

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse(
                {
                    "message": json.dumps(e),
                    "resource": {
                        "cloud_service_group": cloud_service_group,
                        "cloud_service_type": cloud_service_type,
                    },
                }
            )
        else:
            error_resource_response = ErrorResourceResponse(
                {
                    "message": str(e),
                    "resource": {
                        "cloud_service_group": cloud_service_group,
                        "cloud_service_type": cloud_service_type,
                    },
                }
            )

        return error_resource_response
