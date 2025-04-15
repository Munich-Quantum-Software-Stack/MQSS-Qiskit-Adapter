"""Module to test the MQSS Qiskit Adapter"""

from mqss_client import MQSSClient  # type: ignore

from mqss.qiskit_adapter import MQSSQiskitAdapter  # type: ignore


def test_adapter():
    """Test the MQSSQiskitAdapter"""
    adapter = MQSSQiskitAdapter(token="test")
    assert isinstance(adapter.client, MQSSClient)  # pylint: disable=protected-access


def test_adapter_get_backend(_mock_resource_info):
    """Test the MQSSQiskitAdapter get_backend"""
    adapter = MQSSQiskitAdapter(token="test")
    backend = adapter.get_backend(name="res_cmap")
    assert backend.name == "res_cmap"


def test_adapter_backends_all(_mock_resources):
    """Test the MQSSQiskitAdapter backends"""
    adapter = MQSSQiskitAdapter(token="test")
    backends = adapter.backends()
    assert len(backends) == 3
    names = [backend.name for backend in backends]
    assert "res_cmap" in names
    assert "res_no_cmap" in names
    assert "res_offline" in names


def test_adapter_backends_online(_mock_resources):
    """Test the MQSSQiskitAdapter backends"""
    adapter = MQSSQiskitAdapter(token="test")
    backends = adapter.backends(online_backends=True)
    assert len(backends) == 2
    names = [backend.name for backend in backends]
    assert "res_cmap" in names
    assert "res_no_cmap" in names
    assert "res_offline" not in names


def test_adapter_backends_name(_mock_resources):
    """Test the MQSSQiskitAdapter backends"""
    adapter = MQSSQiskitAdapter(token="test")
    backends = adapter.backends(name="res_cmap")
    assert len(backends) == 1
    assert backends[0].name == "res_cmap"


def test_adapter_backends_offline_name(_mock_resources):
    """Test the MQSSQiskitAdapter backends"""
    adapter = MQSSQiskitAdapter(token="test")
    backends = adapter.backends(name="res_offline", online_backends=True)
    assert len(backends) == 0
