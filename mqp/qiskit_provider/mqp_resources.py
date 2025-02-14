"""MQP Resources"""

from mqp_client import ResourceInfo  # type: ignore
from qiskit.circuit.library import Measure  # type: ignore
from qiskit.circuit.library import RXGate  # type: ignore
from qiskit.circuit.library import (  # type: ignore
    CXGate,
    CZGate,
    HGate,
    IGate,
    RGate,
    RXXGate,
    RYGate,
    RZGate,
    XGate,
    YGate,
    ZGate,
)
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
            target.add_instruction(instruction_map[_instruction](), _connections)

    return target


def handle_r():
    """Handle R gate"""
    return RGate(Parameter("theta"), Parameter("phi"))


def handle_id():
    """Handle I gate"""
    return IGate()


def handle_cx():
    """Handle CX gate"""
    return CXGate()


def handle_cz():
    """Handle CZ gate"""
    return CZGate()


def handle_rxx():
    """Handle RXX gate"""
    return RXXGate(Parameter("theta"))


def handle_rx():
    """Handle RX gate"""
    return RXGate(Parameter("theta"))


def handle_ry():
    """Handle RY gate"""
    return RYGate(Parameter("theta"))


def handle_rz():
    """Handle RZ gate"""
    return RZGate(Parameter("lambda"))


def handle_h():
    """Handle H gate"""
    return HGate()


def handle_x():
    """Handle X gate"""
    return XGate()


def handle_y():
    """Handle Y gate"""
    return YGate()


def handle_z():
    """Handle Z gate"""
    return ZGate()


def handle_measure():
    """Handle Measure gate"""
    return Measure()


instruction_map = {
    "r": handle_r,
    "id": handle_id,
    "cz": handle_cz,
    "rz": handle_rz,
    "rx": handle_rx,
    "rxx": handle_rxx,
    "measure": handle_measure,
    "cx": handle_cx,
    "ry": handle_ry,
    "h": handle_h,
    "x": handle_x,
    "y": handle_y,
    "z": handle_z,
}
