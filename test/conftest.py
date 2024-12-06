""""Nodule to define fixtures for the tests"""

import pytest

from .mocks import MockMQPClient


@pytest.fixture
def _mock_resource_info(monkeypatch):
    """Mock the resource info"""
    monkeypatch.setattr(
        "mqp_client.MQPClient.get_resource_info", MockMQPClient.get_resource_info
    )


@pytest.fixture
def _mock_resources(monkeypatch):
    """Mock the resources"""
    monkeypatch.setattr("mqp_client.MQPClient.resources", MockMQPClient.resources)
