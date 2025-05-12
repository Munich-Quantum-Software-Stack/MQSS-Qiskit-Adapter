# ------------------------------------------------------------------------------
# Copyright 2024 Munich Quantum Software Stack Project
#
# Licensed under the Apache License, Version 2.0 with LLVM Exceptions (the
# "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://github.com/Munich-Quantum-Software-Stack/QDMI/blob/develop/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# ------------------------------------------------------------------------------

"""MQSS Qiskit Job Module
This module defines the MQSSQiskitJob class, which extends Qiskit's JobV1 class to manage job
cancellation, status retrieval, and result fetching for MQSS backends using the MQSSClient.
"""

from mqss_client import CircuitJobRequest  # type: ignore
from mqss_client import MQSSClient  # type: ignore
from mqss_client import JobStatus as MQSSJobStatus  # type: ignore
from qiskit.providers import JobStatus  # type: ignore
from qiskit.providers import Backend, JobV1  # type: ignore
from qiskit.result import Counts, Result  # type: ignore


class MQSSQiskitJob(JobV1):
    """MQSSQiskitJob Class: This class is used to manage jobs. Users do not need to create
    an instance of this class directly; it is created and returned by the MQSSQiskitBackend
    when a job is submitted via MQSSQiskitBackend.run."""

    def __init__(
        self, backend: Backend, job_id: str, job_request: CircuitJobRequest, **kwargs
    ) -> None:
        super().__init__(backend, job_id, **kwargs)
        self.client: MQSSClient = backend.client
        self.job_request: CircuitJobRequest = job_request

    def submit(self):
        return NotImplementedError("Submit jobs via the MQSSQiskitJob class.")

    def cancel(self):
        """Cancel the job"""
        self.client.cancel_job(self.job_id(), self.job_request)

    def status(self) -> JobStatus:
        """Return the job's current status

        Returns:
            The status of the job.
            ([JobStatus](https://qiskit.org/documentation/stubs/qiskit.providers.JobStatus.html)).

        """
        mqss_status = self.client.job_status(self.job_id(), self.job_request)
        if mqss_status == MQSSJobStatus.PENDING:
            return JobStatus.INITIALIZING
        if mqss_status == MQSSJobStatus.WAITING:
            return JobStatus.QUEUED
        if mqss_status == MQSSJobStatus.CANCELLED:
            return JobStatus.CANCELLED
        if mqss_status == MQSSJobStatus.FAILED:
            return JobStatus.ERROR
        if mqss_status == MQSSJobStatus.COMPLETED:
            return JobStatus.DONE
        raise RuntimeWarning(f"Unknown job status: {mqss_status}.")

    def result(self) -> Result:
        """Return the result for the job

        Returns:
            [Result](https://qiskit.org/documentation/stubs/qiskit.result.Result.html)
            object for the job.
        """
        res = self.client.wait_for_job_result(self.job_id(), self.job_request)
        if isinstance(res.counts, list):
            res_counts = res.counts
        else:
            res_counts = [res.counts]
        result_dict = {
            "backend_name": self.backend().name,
            "backend_version": None,
            "qobj_id": None,
            "job_id": self.job_id(),
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
