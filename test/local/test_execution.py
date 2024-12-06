"""Unit Tests"""

import pytest
from qiskit import QuantumCircuit, compiler  # type: ignore
from qiskit.providers import JobStatus as QiskitJobStatus  # type: ignore

from mqp.qiskit_provider import MQPProvider

from .config import BACKENDS, TOKEN, URL

simple_circ = QuantumCircuit(2, 2)
simple_circ.h(0)
simple_circ.cx(0, 1)
simple_circ.measure_all()

simple_circ2 = QuantumCircuit(2, 2)
simple_circ2.h(1)
simple_circ2.h(0)
simple_circ2.cx(1, 0)
simple_circ2.measure_all()


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_submit_job():
    """Test job submission and transpiled at backend"""
    provider = MQPProvider(token=TOKEN, url=URL)
    # get some backend
    available_backends = [_b.name for _b in provider.backends()]
    final_backends = [b for b in available_backends if b in BACKENDS]
    print(f"submit_job : {final_backends}")
    for b_name in final_backends:
        backend = provider.get_backend(b_name)
        job = backend.run(simple_circ, shots=200)
        try:
            print(f"{backend.name} : {job.result().get_counts()}")
            assert job.status() == QiskitJobStatus.DONE
        except RuntimeError as _err:
            assert str(_err).find("offline") > -1
            print(f"{backend.name} : offline")


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_submit_batch_job():
    """Test job submission and transpiled at backend"""
    provider = MQPProvider(token=TOKEN, url=URL)
    available_backends = [_b.name for _b in provider.backends()]
    final_backends = [b for b in available_backends if b in BACKENDS]
    print(f"submit_batch_job : {final_backends}")
    for b_name in final_backends:
        backend = provider.get_backend(b_name)
        bjob = backend.run([simple_circ, simple_circ2], shots=200)
        try:
            print(f"{backend.name} : {bjob.result().get_counts()}")
            assert bjob.status() == QiskitJobStatus.DONE
        except RuntimeError as _err:
            assert str(_err).find("offline") > -1
            print(f"{backend.name} : offline")


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_cancel_job():
    """Test job cancellation"""
    provider = MQPProvider(token=TOKEN, url=URL)
    for backend in provider.backends():
        print(f"cancel_job : {backend.name}")
        job = backend.run(simple_circ, shots=200)
        job.cancel()
        assert job.status() == QiskitJobStatus.CANCELLED
        break


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_submit_transpiled_job():
    """Test transpiled job submission and no transpilation at backend"""
    provider = MQPProvider(token=TOKEN, url=URL)
    available_backends = [_b.name for _b in provider.backends()]
    final_backends = [b for b in available_backends if b in BACKENDS]
    print(f"submit_transpiled_job : {final_backends}")
    for backend_name in final_backends:
        backend = provider.get_backend(backend_name)
        transpiled_circ = compiler.transpile(simple_circ, backend, optimization_level=3)
        print(f"{backend.name} : {transpiled_circ is not None}")
        job = backend.run(transpiled_circ, shots=100, no_modify=True)
        try:
            print(f"{backend_name} : {job.result().get_counts()}")
            assert job.status() == QiskitJobStatus.DONE
        except RuntimeError as _err:
            assert str(_err).find("offline") > -1
            print(f"{backend.name} : offline")


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_get_backend():
    """Test get_backend for all backends"""
    provider = MQPProvider(token=TOKEN, url=URL)
    for backend_name in BACKENDS:
        backend = provider.get_backend(backend_name)
        print(backend_name)
        assert backend.name == backend_name


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_backends_name():
    """Test get_backend for all backends"""
    provider = MQPProvider(token=TOKEN, url=URL)
    for backend_name in BACKENDS:
        backend = provider.backends(name=backend_name)
        assert len(backend) == 1
        assert backend[0].name == backend_name


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_backends_online():
    """Test get_backend for all backends"""
    provider = MQPProvider(token=TOKEN, url=URL)
    backend = provider.backends(online_backends=True)
    backend_names = [b.name for b in backend]
    print(f"online_backends : {backend_names}")


@pytest.mark.skipif(TOKEN is None, reason="MQP_TOKEN not provided")
def test_transpiler():
    """Test transpilation only at user side"""
    provider = MQPProvider(token=TOKEN, url=URL)
    available_backends = [_b.name for _b in provider.backends()]
    final_backends = [b for b in available_backends if b in BACKENDS]
    print(f"transpiler : {final_backends}")
    for backend_name in final_backends:
        backend = provider.get_backend(backend_name)
        assert backend.name == backend_name
        transpiled_circ = compiler.transpile(simple_circ, backend, optimization_level=3)
        print(f"{backend.name} : {transpiled_circ is not None}")
        # print(simple_circ.draw())
        # print(transpiled_circ.draw())
        assert transpiled_circ is not None
