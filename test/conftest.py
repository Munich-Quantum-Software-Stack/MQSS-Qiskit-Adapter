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

"""Testing Configuration"""

import os

import pytest
from qiskit.circuit import QuantumCircuit  # type: ignore

from mqss.qiskit_adapter import MQSSQiskitAdapter  # type: ignore

TOKEN = None
try:
    TOKEN = os.environ["MQP_TOKEN"]
except KeyError:
    print("set MQP_TOKEN to your MQP token in the environment.")

# NOTE: change to current backend names
BACKENDS = ["QExa20", "AQT20"]
URL = "https://portal.quantum.lrz.de:4000"


@pytest.mark.skipif(TOKEN is None, reason="MQSS token not provided")
@pytest.fixture
def mqss_adapter():
    """Setup MQSSQiskitAdapter for tests."""
    return MQSSQiskitAdapter(token=TOKEN, hpcqc=False, base_url=URL)


@pytest.fixture
def test_circuit():
    """Test circuit."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc


@pytest.fixture
def test_circuit_batch():
    """Test circuits for batch processing."""
    qc1 = QuantumCircuit(2)
    qc1.h(0)
    qc1.cx(0, 1)
    qc1.measure_all()
    qc2 = QuantumCircuit(2)
    qc2.h(0)
    qc2.h(1)
    qc2.cx(0, 1)
    qc2.measure_all()
    return [qc1, qc2]
