"""MQP Backend Module"""

from typing import List, Optional, Union

from mqp_client import MQPClient, ResourceInfo  # type: ignore
from qiskit.circuit import QuantumCircuit  # type: ignore
from qiskit.providers import BackendV2, Options  # type: ignore
from qiskit.qasm2 import dumps as qasm_str  # type: ignore
from qiskit.transpiler import CouplingMap, Target  # type: ignore

from .job import MQPJob
from .mqp_resources import get_coupling_map, get_target


class MQPBackend(BackendV2):
    """MQP Backend class"""

    def __init__(
        self,
        name: str,
        client: MQPClient,
        resource_info: Optional[ResourceInfo] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.client = client
        _resource_info = resource_info or self.client.get_resource_info(self.name)
        assert _resource_info is not None
        self._coupling_map = get_coupling_map(_resource_info)
        self._target = get_target(_resource_info)

    @classmethod
    def _default_options(cls) -> Options:
        return Options(
            shots=1024, qubit_mapping=None, calibration_set_id=None, no_modify=False
        )

    @property
    def coupling_map(self) -> CouplingMap:
        """Return the CouplingMap for the backend"""
        return self._coupling_map

    @property
    def target(self) -> Target:
        """Return the Target for the backend"""
        if self._target is None:
            raise NotImplementedError(f"Target for {self.name} is not available.")
        return self._target

    @property
    def max_circuits(self) -> Optional[int]:
        return None

    def run(
        self,
        run_input: Union[QuantumCircuit, List[QuantumCircuit]],
        shots: int = 10000,
        no_modify: bool = False,
        **options,
    ) -> MQPJob:
        """Run a circuit on the backend

        Args:
            run_input (Union[QuantumCircuit, List[QuantumCircuit]]): quantum circuit(s) to run
            shots (int): number of shots (default: 10000)
            no_modify (bool): do not modify/transpile the circuit (default: False)

        Returns:
            MQPJob: job instance
        """

        if isinstance(run_input, QuantumCircuit):
            _circuits = str([qasm_str(run_input)])
        else:
            _circuits = str([qasm_str(qc) for qc in run_input])
        _circuit_format = "qasm"

        job_id = self.client.submit_job(
            resource_name=self.name,
            circuit=_circuits,
            circuit_format=_circuit_format,
            shots=shots,
            no_modify=no_modify,
        )
        return MQPJob(self.client, job_id)


# circuit=b64encode(pickle_dumps(circuits)).decode(encoding="ascii"),
