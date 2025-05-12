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

"""Module to test the MQSS Qiskit Backend."""

import pytest
from mqss_client import MQSSClient  # type: ignore
from qiskit import compiler  # type: ignore
from qiskit.providers import JobStatus as QiskitJobStatus  # type: ignore

from mqss.qiskit_adapter import MQSSQiskitAdapter, MQSSQiskitBackend, MQSSQiskitJob

from .conftest import (
    TEST_BACKEND,
)


class TestMQSSQiskitBackend:
    """Test the MQSSQiskitBackend."""

    @pytest.fixture
    def mqss_backend(self, mqss_adapter):
        """Setup MQSSQiskitBackend for tests."""
        assert mqss_adapter is not None
        [mqss_backend] = mqss_adapter.backends(name=TEST_BACKEND, online=True)
        return mqss_backend

    @pytest.mark.backend
    def test_init(self, mqss_backend):
        """Test the MQSSQiskitBackend"""
        assert mqss_backend.client is not None
        assert isinstance(mqss_backend.client, MQSSClient)
        assert mqss_backend.name == TEST_BACKEND

    @pytest.mark.backend
    def test_transpiler(self, mqss_adapter, test_circuit):
        """Test the MQSSQiskitBackend transpiler"""
        assert mqss_adapter is not None
        assert isinstance(mqss_adapter, MQSSQiskitAdapter)
        for backend in mqss_adapter.backends():
            assert isinstance(backend, MQSSQiskitBackend)
            assert backend.name is not None
            if backend._target is None:
                # Skip if the target is not available
                continue
            transpiled_circuit = compiler.transpile(
                test_circuit, backend, optimization_level=3
            )
            assert transpiled_circuit is not None

    @pytest.mark.job
    def test_run_job(self, mqss_backend, test_circuit):
        """Test the MQSSQiskitBackend run job"""
        assert mqss_backend is not None
        assert isinstance(mqss_backend, MQSSQiskitBackend)

        job = mqss_backend.run(test_circuit, shots=100)
        assert job is not None
        assert isinstance(job, MQSSQiskitJob)
        result = job.result().get_counts()
        assert result is not None
        assert isinstance(result, dict)
        assert job.status() == QiskitJobStatus.DONE

    @pytest.mark.job
    def test_run_job_batch(self, mqss_backend, test_circuit_batch):
        """Test the MQSSQiskitBackend run job batch"""
        assert mqss_backend is not None
        assert isinstance(mqss_backend, MQSSQiskitBackend)

        job = mqss_backend.run(test_circuit_batch, shots=100)
        assert job is not None
        assert isinstance(job, MQSSQiskitJob)
        assert len(job.result().get_counts()) == len(test_circuit_batch)
        for result in job.result().get_counts():
            assert result is not None
            assert isinstance(result, dict)
        assert job.status() == QiskitJobStatus.DONE

    @pytest.mark.job
    def test_run_job_transpiled(self, mqss_backend, test_circuit):
        """Test the MQSSQiskitBackend run job transpiled"""
        assert mqss_backend is not None
        assert isinstance(mqss_backend, MQSSQiskitBackend)

        transpiled_circuit = compiler.transpile(
            test_circuit, mqss_backend, optimization_level=3
        )
        assert transpiled_circuit is not None
        job = mqss_backend.run(transpiled_circuit, shots=100, no_modify=True)
        assert job is not None
        assert isinstance(job, MQSSQiskitJob)
        result = job.result().get_counts()
        assert result is not None
        assert isinstance(result, dict)
        assert job.status() == QiskitJobStatus.DONE

    @pytest.mark.job
    def test_run_job_qasm3(self, mqss_backend, test_circuit):
        """Test the MQSSQiskitBackend run job with QASM3"""
        assert mqss_backend is not None
        assert isinstance(mqss_backend, MQSSQiskitBackend)

        job = mqss_backend.run(test_circuit, shots=100, qasm3=True)
        assert job is not None
        assert isinstance(job, MQSSQiskitJob)
        result = job.result().get_counts()
        assert result is not None
        assert isinstance(result, dict)
        assert job.status() == QiskitJobStatus.DONE
