"""MQPJob Module
This module defines the MQPJob class, which extends Qiskit's JobV1 class to manage job
cancellation, status retrieval, and result fetching for MQP backends using the MQPClient.
"""

from mqp_client import JobStatus as MQPJobStatus  # type: ignore
from mqp_client import MQPClient
from qiskit.providers import JobStatus  # type: ignore
from qiskit.providers import JobV1  # type: ignore
from qiskit.result import Counts, Result  # type: ignore


class MQPJob(JobV1):
    """MQPJob Class: This class is used to manage jobs. Users do not need to create
    an instance of this class directly; it is created and returned by the MQPBackend
    when a job is submitted via MQPBackend.run."""

    def __init__(self, client: MQPClient, job_id: str, **kwargs) -> None:
        super().__init__(None, job_id, **kwargs)
        self.client = client

    def submit(self):
        return NotImplementedError("Submit jobs via the MQPClient")

    def cancel(self):
        """Cancel the job"""
        self.client.cancel(self.job_id())

    def status(self) -> JobStatus:
        """Return the job's current status

        Returns:
            The status of the job.
            ([JobStatus](https://qiskit.org/documentation/stubs/qiskit.providers.JobStatus.html)).

        """
        mqp_status = self.client.status(self.job_id())
        if mqp_status == MQPJobStatus.PENDING:
            return JobStatus.INITIALIZING
        if mqp_status == MQPJobStatus.WAITING:
            return JobStatus.QUEUED
        if mqp_status == MQPJobStatus.CANCELLED:
            return JobStatus.CANCELLED
        if mqp_status == MQPJobStatus.FAILED:
            return JobStatus.ERROR
        if mqp_status == MQPJobStatus.COMPLETED:
            return JobStatus.DONE
        raise RuntimeWarning(f"Unknown job status: {mqp_status}.")

    def result(self) -> Result:
        """Return the result for the job

        Returns:
            [Result](https://qiskit.org/documentation/stubs/qiskit.result.Result.html)
            object for the job.
        """
        res = self.client.wait_for_result(self.job_id())
        if isinstance(res.counts, list):
            res_counts = res.counts
        else:
            res_counts = [res.counts]
        result_dict = {
            "backend_name": None,
            "backend_version": None,
            "qobj_id": None,
            "job_id": self._job_id,
            "success": True,
            "results": [
                {
                    "shots": sum(_counts.values()),
                    "success": True,
                    "data": {
                        "counts": Counts(_counts),
                    },
                }
                for _counts in res_counts
            ],
            "timestamps": {
                "submitted": res.timestamp_submitted,
                "scheduled": res.timestamp_scheduled,
                "completed": res.timestamp_completed,
            },
        }
        return Result.from_dict(result_dict)
