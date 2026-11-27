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

"""Mocked tests: the adapter against an in-memory MQP, no token or network.

These run in CI on every pull request. The `backend` and `job` tests in the
other modules exercise the real service and need an MQSS token.
"""

import ast

import pytest
from mqss_client import JobStatus as MQSSJobStatus  # type: ignore
from mqss_client import MQSSClient  # type: ignore
from mqss_client.hpc_client import HPCOffloadClient  # type: ignore
from mqss_client.rest_client import RESTClient  # type: ignore
from qiskit import compiler  # type: ignore
from qiskit.providers import JobStatus  # type: ignore
from qiskit.transpiler import CouplingMap, Target  # type: ignore

from mqss.qiskit_adapter import MQSSQiskitAdapter, MQSSQiskitBackend, MQSSQiskitJob

from .mock_mqp import MockMQP

pytestmark = pytest.mark.mock


@pytest.fixture
def mock_mqp():
    """In-memory MQP transport."""
    return MockMQP()


@pytest.fixture
def adapter(mock_mqp):
    """Adapter whose client talks to the in-memory MQP."""
    _adapter = MQSSQiskitAdapter(token="fake-token", base_url="http://mqp.invalid")
    _adapter.client.client = mock_mqp
    return _adapter


@pytest.fixture
def backend(adapter):
    """The online mock device."""
    return adapter.get_backend("MockQPU")


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """Skip the polling delay of MQSSClient.wait_for_job_result."""
    monkeypatch.setattr("mqss_client.mqss_client.time.sleep", lambda _: None)


# -- adapter ----------------------------------------------------------------


class TestAdapter:
    """MQSSQiskitAdapter construction and backend discovery."""

    def test_rest_client_by_default(self, monkeypatch):
        """Without hpcqc the adapter talks to the REST API."""
        monkeypatch.delenv("MQSS_HPCQC_ENV", raising=False)
        _adapter = MQSSQiskitAdapter(token="t", base_url="http://mqp.invalid")
        assert isinstance(_adapter.client, MQSSClient)
        assert isinstance(_adapter.client.client, RESTClient)
        assert _adapter.client.client.url == "http://mqp.invalid"

    def test_hpcqc_argument(self, monkeypatch):
        """hpcqc=True selects the HPC offload client."""
        monkeypatch.delenv("MQSS_HPCQC_ENV", raising=False)
        _adapter = MQSSQiskitAdapter(token="t", hpcqc=True)
        assert isinstance(_adapter.client.client, HPCOffloadClient)

    @pytest.mark.parametrize("value", ["true", "1", "T"])
    def test_hpcqc_environment(self, monkeypatch, value):
        """MQSS_HPCQC_ENV selects the HPC offload client."""
        monkeypatch.setenv("MQSS_HPCQC_ENV", value)
        _adapter = MQSSQiskitAdapter(token="t")
        assert isinstance(_adapter.client.client, HPCOffloadClient)

    def test_hpcqc_argument_overrides_environment(self, monkeypatch):
        """An explicit hpcqc=False wins over MQSS_HPCQC_ENV."""
        monkeypatch.setenv("MQSS_HPCQC_ENV", "true")
        _adapter = MQSSQiskitAdapter(token="t", hpcqc=False, base_url="http://x")
        assert isinstance(_adapter.client.client, RESTClient)

    def test_get_backend_nameless(self, adapter):
        """A nameless backend has neither coupling map nor target."""
        _backend = adapter.get_backend()
        assert isinstance(_backend, MQSSQiskitBackend)
        assert _backend.name is None
        assert _backend.coupling_map is None
        with pytest.raises(NotImplementedError):
            _ = _backend.target

    def test_get_backend_by_name(self, adapter):
        """A named backend is built from its resource info."""
        _backend = adapter.get_backend(name="MockQPU")
        assert _backend.name == "MockQPU"
        assert _backend.client is adapter.client

    def test_get_backend_invalid(self, adapter):
        """An unknown backend name raises."""
        with pytest.raises(ValueError):
            adapter.get_backend(name="does-not-exist")

    def test_backends_all(self, adapter):
        """All resources are returned."""
        names = sorted(b.name for b in adapter.backends())
        assert names == ["MockOffline", "MockQPU"]

    def test_backends_online(self, adapter):
        """online=True filters out offline resources."""
        assert [b.name for b in adapter.backends(online=True)] == ["MockQPU"]

    def test_backends_by_name(self, adapter):
        """name= returns just that resource."""
        [_backend] = adapter.backends(name="MockOffline")
        assert _backend.name == "MockOffline"

    def test_backends_invalid_name(self, adapter):
        """An unknown name raises."""
        with pytest.raises(ValueError):
            adapter.backends(name="does-not-exist")

    def test_backends_none(self, adapter, monkeypatch):
        """No resource list from the service gives no backends."""
        monkeypatch.setattr(adapter.client, "get_all_resources", lambda: None)
        assert not adapter.backends()


# -- backend ----------------------------------------------------------------


class TestBackend:
    """MQSSQiskitBackend properties and target construction."""

    def test_coupling_map(self, backend):
        """The coupling map follows the resource connectivity."""
        assert isinstance(backend.coupling_map, CouplingMap)
        assert sorted(backend.coupling_map.get_edges()) == [
            (0, 1),
            (1, 0),
            (1, 2),
            (2, 1),
        ]

    def test_target(self, capsys, backend):
        """Known instructions land in the target, unknown ones are reported."""
        target = backend.target
        assert isinstance(target, Target)
        assert target.num_qubits == 3
        for name in ("cx", "cz", "rz", "measure", "reset", "if_else", "swap"):
            assert name in target.operation_names
        assert "unknown_gate" not in target.operation_names
        assert "unknown_gate" in capsys.readouterr().out

    def test_offline_backend_without_target(self, adapter):
        """A resource without instructions has no target."""
        _backend = adapter.get_backend("MockOffline")
        assert _backend.coupling_map is None
        with pytest.raises(NotImplementedError):
            _ = _backend.target

    def test_options_and_limits(self, backend):
        """Default options and circuit limit."""
        assert backend.options.shots == 1024
        assert backend.options.no_modify is False
        assert backend.max_circuits is None

    def test_num_pending_jobs(self, backend, mock_mqp):
        """Pending jobs come from the service."""
        assert backend.num_pending_jobs == mock_mqp.pending_jobs

    def test_transpile(self, backend, test_circuit):
        """Circuits transpile against the backend target."""
        transpiled = compiler.transpile(test_circuit, backend, optimization_level=3)
        assert transpiled.num_qubits == 3


# -- jobs -------------------------------------------------------------------


class TestJob:
    """Job submission, status, cancellation and results."""

    @pytest.mark.parametrize(
        "qasm3, circuit_format", [(True, "qasm3"), (False, "qasm")]
    )
    def test_run_single(self, backend, mock_mqp, test_circuit, qasm3, circuit_format):
        """A single circuit is serialized and its counts returned."""
        job = backend.run(test_circuit, shots=100, qasm3=qasm3)
        assert isinstance(job, MQSSQiskitJob)
        request = mock_mqp.jobs[job.job_id()]["request"]
        assert request["circuit_format"] == circuit_format
        assert request["resource_name"] == "MockQPU"
        assert request["shots"] == 100
        assert len(ast.literal_eval(request["circuit"])) == 1
        assert job.result().get_counts() == {"00": 50, "11": 50}
        assert job.status() == JobStatus.DONE

    @pytest.mark.parametrize("qasm3", [True, False])
    def test_run_batch(self, backend, mock_mqp, test_circuit_batch, qasm3):
        """A batch is sent as one job and returns one count dict per circuit."""
        job = backend.run(test_circuit_batch, shots=10, qasm3=qasm3)
        request = mock_mqp.jobs[job.job_id()]["request"]
        assert len(ast.literal_eval(request["circuit"])) == len(test_circuit_batch)
        counts = job.result().get_counts()
        assert counts == [{"00": 5, "11": 5}, {"00": 5, "11": 5}]

    def test_run_flags(self, backend, mock_mqp, test_circuit):
        """no_modify and queued are passed through."""
        job = backend.run(test_circuit, no_modify=True, queued=True)
        request = mock_mqp.jobs[job.job_id()]["request"]
        assert request["no_modify"] is True
        assert request["queued"] is True
        assert request["shots"] == 1024

    def test_run_mid_circuit_measurement(
        self, backend, test_circuit_mid_circuit_measurements
    ):
        """Dynamic circuits serialize to QASM3."""
        job = backend.run(test_circuit_mid_circuit_measurements, shots=4)
        assert job.result().get_counts() == {"00": 2, "11": 2}

    def test_result_waits_for_completion(self, adapter, test_circuit):
        """result() polls until the job leaves PENDING/WAITING."""
        mock = MockMQP(status_sequence=["PENDING", "WAITING", "COMPLETED"])
        adapter.client.client = mock
        job = adapter.get_backend("MockQPU").run(test_circuit, shots=2)
        assert job.result().get_counts() == {"00": 1, "11": 1}
        assert mock.jobs[job.job_id()]["status_calls"] == 3

    @pytest.mark.parametrize(
        "mqss_status, qiskit_status",
        [
            ("PENDING", JobStatus.INITIALIZING),
            ("WAITING", JobStatus.QUEUED),
            ("CANCELLED", JobStatus.CANCELLED),
            ("FAILED", JobStatus.ERROR),
            ("COMPLETED", JobStatus.DONE),
        ],
    )
    def test_status_mapping(self, adapter, test_circuit, mqss_status, qiskit_status):
        """MQSS statuses map onto Qiskit statuses."""
        adapter.client.client = MockMQP(status_sequence=[mqss_status])
        job = adapter.get_backend("MockQPU").run(test_circuit)
        assert job.status() == qiskit_status

    def test_status_unknown(self, backend, test_circuit, monkeypatch):
        """A status the adapter does not know raises."""
        job = backend.run(test_circuit)
        monkeypatch.setattr(job.client, "job_status", lambda *_: "SOMETHING_ELSE")
        with pytest.raises(RuntimeWarning):
            job.status()

    @pytest.mark.parametrize("final_status", ["FAILED", "CANCELLED"])
    def test_result_of_unsuccessful_job(self, adapter, test_circuit, final_status):
        """result() raises when the job did not complete."""
        adapter.client.client = MockMQP(status_sequence=[final_status])
        job = adapter.get_backend("MockQPU").run(test_circuit)
        with pytest.raises(RuntimeError):
            job.result()

    def test_cancel(self, backend, mock_mqp, test_circuit):
        """cancel() deletes the job on the service."""
        job = backend.run(test_circuit)
        job.cancel()
        assert mock_mqp.cancelled == [job.job_id()]
        assert f"DELETE job/{job.job_id()}" in mock_mqp.requests

    def test_submit_not_supported(self, backend, test_circuit):
        """Jobs are submitted through the backend, not the job."""
        job = backend.run(test_circuit)
        assert isinstance(job.submit(), NotImplementedError)

    def test_status_enum_is_mqss(self):
        """The mock speaks the same status vocabulary as mqss_client."""
        assert {s.value for s in MQSSJobStatus} >= {
            "PENDING",
            "WAITING",
            "FAILED",
            "COMPLETED",
            "CANCELLED",
        }
