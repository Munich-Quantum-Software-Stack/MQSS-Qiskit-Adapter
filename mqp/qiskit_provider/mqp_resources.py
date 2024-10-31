"""MQP Resources"""

from mqp_client import ResourceInfo  # type: ignore
from qiskit.circuit.library import Measure  # type: ignore
from qiskit.circuit.library import RXGate  # type: ignore
from qiskit.circuit.library import CZGate, IGate, RGate, RXXGate, RZGate  # type: ignore
from qiskit.circuit.parameter import Parameter  # type: ignore
from qiskit.transpiler import CouplingMap, Target  # type: ignore


def get_coupling_map(resource_info: ResourceInfo):
    """Return CouplingMap for the backend"""

    return (
        CouplingMap(couplinglist=resource_info.connectivity)
        if resource_info is not None and resource_info.connectivity is not None
        else None
    )


def get_target(resource_info: ResourceInfo):
    """Return Target for the backend"""

    target = (
        Target(num_qubits=resource_info.qubits) if resource_info is not None else None
    )

    if resource_info is not None and resource_info.instructions is not None:
        assert target is not None
        for _instruction, _connections in resource_info.instructions:
            if _instruction == "r":
                target.add_instruction(
                    RGate(Parameter("theta"), Parameter("phi")), _connections
                )
            if _instruction == "id":
                target.add_instruction(IGate(), _connections)
            if _instruction == "cz":
                target.add_instruction(CZGate(), _connections)
            if _instruction == "rz":
                target.add_instruction(RZGate(Parameter("lambda")), _connections)
            if _instruction == "rx":
                target.add_instruction(RXGate(Parameter("theta")), _connections)
            if _instruction == "rxx":
                target.add_instruction(RXXGate(Parameter("theta")), _connections)
            if _instruction == "measure":
                target.add_instruction(Measure(), _connections)

    return target
