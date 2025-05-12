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

"""MQP Resources"""

from mqss_client import ResourceInfo  # type: ignore
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
        Target(num_qubits=resource_info.qubits)
        if resource_info is not None and resource_info.instructions is not None
        else None
    )

    if resource_info is not None and resource_info.instructions is not None:
        assert target is not None

        for _instruction, _connections in resource_info.instructions:
            try:
                target.add_instruction(instruction_map[_instruction](), _connections)
            except KeyError:
                print(
                    f"Warning: Instruction '{_instruction}' not found in the instruction_map."
                )

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
