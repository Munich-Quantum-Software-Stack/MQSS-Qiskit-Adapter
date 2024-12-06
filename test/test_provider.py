"""Module to test the MQP Provider"""

from mqp_client import MQPClient  # type: ignore

from mqp.qiskit_provider import MQPProvider


def test_provider():
    """Test the MQPProvider"""
    provider = MQPProvider(token="test")
    assert isinstance(provider._client, MQPClient)  # pylint: disable=protected-access


def test_provider_get_backend(_mock_resource_info):
    """Test the MQPProvider get_backend"""
    provider = MQPProvider(token="test")
    backend = provider.get_backend(name="res_cmap")
    assert backend.name == "res_cmap"


def test_provider_backends_all(_mock_resources):
    """Test the MQPProvider backends"""
    provider = MQPProvider(token="test")
    backends = provider.backends()
    assert len(backends) == 3
    names = [backend.name for backend in backends]
    assert "res_cmap" in names
    assert "res_no_cmap" in names
    assert "res_offline" in names


def test_provider_backends_online(_mock_resources):
    """Test the MQPProvider backends"""
    provider = MQPProvider(token="test")
    backends = provider.backends(online_backends=True)
    assert len(backends) == 2
    names = [backend.name for backend in backends]
    assert "res_cmap" in names
    assert "res_no_cmap" in names
    assert "res_offline" not in names


def test_provider_backends_name(_mock_resources):
    """Test the MQPProvider backends"""
    provider = MQPProvider(token="test")
    backends = provider.backends(name="res_cmap")
    assert len(backends) == 1
    assert backends[0].name == "res_cmap"


def test_provider_backends_offline_name(_mock_resources):
    """Test the MQPProvider backends"""
    provider = MQPProvider(token="test")
    backends = provider.backends(name="res_offline", online_backends=True)
    assert len(backends) == 0
