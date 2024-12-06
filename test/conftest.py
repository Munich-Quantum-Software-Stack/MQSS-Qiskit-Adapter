import pytest
from .mocks import MockMQPClient


@pytest.fixture
def mock_resource_info(monkeypatch):
    monkeypatch.setattr(
        "mqp_client.MQPClient.get_resource_info", MockMQPClient.get_resource_info
    )


@pytest.fixture
def mock_resources(monkeypatch):
    monkeypatch.setattr("mqp_client.MQPClient.resources", MockMQPClient.resources)


@pytest.fixture
def mock_mqp_client(monkeypatch):
    monkeypatch.setattr("mqp.qiskit_provider.MQPProvider._client", MockMQPClient)
