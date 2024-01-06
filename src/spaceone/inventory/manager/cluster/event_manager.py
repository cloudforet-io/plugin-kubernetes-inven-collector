import logging

from spaceone.inventory.libs.manager import KubernetesManager
from spaceone.inventory.connector.cluster.event import EventConnector
from spaceone.inventory.model.cluster.event.cloud_service import (
    EventResource,
    EventResponse,
)
from spaceone.inventory.model.cluster.event.cloud_service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.model.cluster.event.data import Event

_LOGGER = logging.getLogger(__name__)


class EventManager(KubernetesManager):
    connector_name = "EventConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f"** Event Start **")
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        collected_cloud_services = []
        error_responses = []

        secret_data = params["secret_data"]
        event_name = ""

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        event_conn: EventConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        list_all_event = event_conn.list_event()
        # _LOGGER.debug(f'list_all_event => {list_all_event}')

        for event in list_all_event:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                event_name = event.metadata.name
                cluster_name = self.get_cluster_name(secret_data)
                region = "global"

                _LOGGER.debug(f"event => {event.to_dict()}")
                ##################################
                # 2. Make Base Data
                ##################################
                # key:value type data need to be processed separately
                # Convert object to dict
                raw_data = event.to_dict()
                raw_readonly = event.to_dict()
                raw_data["metadata"]["annotations"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("annotations", {})
                )
                raw_data["metadata"]["labels"] = self.convert_labels_format(
                    raw_readonly.get("metadata", {}).get("labels", {})
                )
                raw_data["uid"] = raw_readonly["metadata"]["uid"]

                labels = raw_data["metadata"]["labels"]

                event_data = Event(raw_data, strict=False)
                _LOGGER.debug(f"event_data => {event_data.to_primitive()}")

                ##################################
                # 3. Make Return Resource
                ##################################
                event_resource = EventResource(
                    {
                        "name": event_name,
                        "account": cluster_name,
                        "tags": labels,
                        "region_code": region,
                        "data": event_data,
                        "reference": event_data.reference(),
                    }
                )

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of InstanceResponse Object
                ##################################
                collected_cloud_services.append(
                    EventResponse({"resource": event_resource})
                )

            except Exception as e:
                _LOGGER.error(f"[collect_cloud_service] => {e}", exc_info=True)
                # Pod name is key
                error_response = self.generate_resource_error_response(
                    e, "Cluster", "Event", event_name
                )
                error_responses.append(error_response)

        return collected_cloud_services, error_responses
