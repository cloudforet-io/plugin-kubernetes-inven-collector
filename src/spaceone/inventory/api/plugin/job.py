import logging
from spaceone.api.inventory.plugin import job_pb2_grpc, job_pb2
from spaceone.core.pygrpc import BaseAPI
from spaceone.inventory.service import JobService

_LOGGER = logging.getLogger(__name__)


class Job(BaseAPI, job_pb2_grpc.JobServicer):
    pb2 = job_pb2
    pb2_grpc = job_pb2_grpc

    def get_tasks(self, request, context):
        params, metadata = self.parse_request(request, context)

        job_svc: JobService = self.locator.get_service("JobService", metadata)

        with job_svc:
            tasks = job_svc.get_tasks(params)
            return self.locator.get_info("TasksInfo", tasks)
