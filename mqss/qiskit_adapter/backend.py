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

"""MQSS Backend Module"""

from typing import List, Optional, Union

from mqss_client import CircuitJobRequest, MQSSClient, ResourceInfo  # type: ignore
from qiskit.circuit import QuantumCircuit  # type: ignore
from qiskit.providers import BackendV2, Options  # type: ignore
from qiskit.qasm2 import dumps as qasm2_str  # type: ignore
from qiskit.qasm3 import dumps as qasm3_str  # type: ignore
from qiskit.transpiler import CouplingMap, Target  # type: ignore

from .job import MQSSQiskitJob
from .mqss_resources import get_coupling_map, get_target


class MQSSQiskitBackend(BackendV2):
    """MQSS Qiskit Backend class: This class extends Qiskit's BackendV2 class
    and provides methods to compile and run circuits on the backend.
    Users do not need to create an instance of this class directly;
    it is created and returned by the MQSSQiskitAdapter when a backend is requested.
    """

    def __init__(
        self,
        client: MQSSClient,
        name: Optional[str] = None,
        resource_info: Optional[ResourceInfo] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.client = client
        _resource_info = resource_info or (
            self.client.get_resource_info(self.name) if name else None
        )
        self._coupling_map = None
        self._target = None
        if _resource_info is not None:
            self._coupling_map = get_coupling_map(_resource_info)
            self._target = get_target(_resource_info)

        if self.name is not None and _resource_info is None:
            raise ValueError(f"{self.name} is not available. ")

    @classmethod
    def _default_options(cls) -> Options:
        return Options(
            shots=1024,
            qubit_mapping=None,
            calibration_set_id=None,
            no_modify=False,
            queued=False,
        )

    @property
    def coupling_map(self) -> CouplingMap:
        """Return the
        [CouplingMap](https://qiskit.org/documentation/stubs/qiskit.transpiler.CouplingMap.html)
        for the backend

        Returns:
            Coupling map for the backend
        """
        return self._coupling_map

    @property
    def target(self) -> Target:
        """Return the [Target](https://qiskit.org/documentation/stubs/qiskit.transpiler.Target.html)
        for the backend

        Returns:
            Target for the backend

        Raises:
            NotImplementedError: Target for the backend is not available/implemented
        """
        if self._target is None:
            raise NotImplementedError(f"Target for {self.name} is not available.")
        return self._target

    @property
    def max_circuits(self) -> Optional[int]:
        return None

    @property
    def num_pending_jobs(self) -> int:
        """Returns the number of jobs waiting to be scheduled on the backend

        Returns:
            Number of pending jobs
        """
        return self.client.get_num_pending_jobs(self.name)

    def run(
        self,
        run_input: Union[QuantumCircuit, List[QuantumCircuit]],
        shots: int = 1024,
        *,
        no_modify: bool = False,
        qasm3: bool = True,
        queued: bool = False,
        **options,
    ) -> MQSSQiskitJob:
        """Submit a circuit/batch of circuits to the backend

        Args:
            run_input (Union[QuantumCircuit, List[QuantumCircuit]]): quantum circuit(s) to run
            shots (int): number of shots
            no_modify (bool): do not modify/transpile the circuit
            qasm3 (bool): use QASM3 format to send the circuit
            queued (bool): enqueue (for limited time) the job while backend is offline

        Returns:
            An instance of MQSSQiskitJob
        """

        if isinstance(run_input, QuantumCircuit):
            _circuits = (
                str([qasm3_str(run_input)]) if qasm3 else str([qasm2_str(run_input)])
            )
        else:
            _circuits = (
                str([qasm3_str(qc) for qc in run_input])
                if qasm3
                else str([qasm2_str(qc) for qc in run_input])
            )
        _circuit_format = "qasm3" if qasm3 else "qasm"

        job_request = CircuitJobRequest(
            circuits=_circuits,
            circuit_format=_circuit_format,
            resource_name=self.name,
            shots=shots,
            no_modify=no_modify,
            queued=queued,
        )

        job_id = self.client.submit_job(job_request)
        return MQSSQiskitJob(self, job_id, job_request)
