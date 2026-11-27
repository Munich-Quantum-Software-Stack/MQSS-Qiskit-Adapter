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

"""In-memory stand-in for the MQP REST API, used by the mocked tests.

It replaces the transport (``MQSSClient.client``) and answers the same paths as
the real service, so the adapter and ``mqss_client`` run unchanged and no
network access or token is needed.
"""

import ast
import json
import uuid
from typing import Any, Dict, List, Optional

from mqss_client.base_client import BaseClient  # type: ignore

TIMESTAMP = "2026-01-01 12:00:00.000000"

# Qubit arguments each instruction is available on, as the service reports them.
ONE_QUBIT = {(0,): None, (1,): None, (2,): None}
TWO_QUBIT = {(0, 1): None, (1, 0): None, (1, 2): None, (2, 1): None}

# Two devices: an online one with a full target and an offline one with only a
# qubit count, so both branches of target construction are exercised.
RESOURCES: Dict[str, Dict[str, Any]] = {
    "MockQPU": {
        "name": "MockQPU",
        "qubits": 3,
        "online": True,
        "connectivity": "[[0, 1], [1, 0], [1, 2], [2, 1]]",
        "instructions": str(
            [(name, ONE_QUBIT) for name in ("r", "id", "rx", "ry", "rz", "x", "y", "z")]
            + [(name, ONE_QUBIT) for name in ("h", "measure", "reset")]
            + [(name, TWO_QUBIT) for name in ("cx", "cz", "rxx", "swap")]
            + [("if_else", None), ("unknown_gate", ONE_QUBIT)]
        ),
    },
    "MockOffline": {
        "name": "MockOffline",
        "qubits": 2,
        "online": False,
    },
}


class MockMQP(BaseClient):  # pylint: disable=too-many-instance-attributes
    """Fake transport answering the MQP REST paths from memory.

    Args:
        status_sequence: statuses a job reports on consecutive status calls;
            the last one repeats. Defaults to an immediately completed job.
    """

    def __init__(self, status_sequence: Optional[List[str]] = None) -> None:
        self.status_sequence = status_sequence or ["COMPLETED"]
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.cancelled: List[str] = []
        self.requests: List[str] = []
        self.pending_jobs = 4

    # -- BaseClient interface -------------------------------------------------

    def get(self, path: str) -> dict:
        self.requests.append(f"GET {path}")
        parts = path.split("/")
        if parts == ["resources"]:
            return RESOURCES
        if parts[0] == "resources" and len(parts) == 2:
            return RESOURCES.get(parts[1], {})
        if parts[0] == "resources" and parts[2:] == ["num_pending_jobs"]:
            return {"num_pending_jobs": self.pending_jobs}
        if parts[0] == "job" and len(parts) == 3:
            job = self.jobs[parts[1]]
            if parts[2] == "status":
                return {"status": self._next_status(job)}
            if parts[2] == "result":
                return self._result(job)
            if parts[2] == "cancel_reason":
                return {"reason": "cancelled by user"}
        raise KeyError(f"Unexpected GET {path}")

    def post(self, path: str, data: dict) -> dict:
        self.requests.append(f"POST {path}")
        if path != "job":
            raise KeyError(f"Unexpected POST {path}")
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {"request": data, "status_calls": 0}
        return {"uuid": job_id}

    def delete(self, path: str) -> None:
        self.requests.append(f"DELETE {path}")
        self.cancelled.append(path.split("/")[1])

    # -- helpers --------------------------------------------------------------

    def _next_status(self, job: Dict[str, Any]) -> str:
        index = min(job["status_calls"], len(self.status_sequence) - 1)
        job["status_calls"] += 1
        return self.status_sequence[index]

    @staticmethod
    def _result(job: Dict[str, Any]) -> Dict[str, str]:
        request = job["request"]
        circuits = ast.literal_eval(request["circuit"])
        shots = request["shots"]
        counts = [{"00": shots // 2, "11": shots - shots // 2} for _ in circuits]
        return {
            # A single circuit is returned as a plain dict, a batch as a list.
            "result": json.dumps(counts[0] if len(counts) == 1 else counts),
            "timestamp_submitted": TIMESTAMP,
            "timestamp_scheduled": TIMESTAMP,
            "timestamp_completed": TIMESTAMP,
        }
