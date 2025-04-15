"""Module to define fixtures for the tests"""

import pytest

from .mocks import MockMQSSClient


@pytest.fixture
def _mock_resource_info(monkeypatch):
    """Mock the get_resource_info"""
    monkeypatch.setattr(
        "mqss_client.MQSSClient.get_resource_info", MockMQSSClient.get_resource_info
    )


@pytest.fixture
def _mock_resources(monkeypatch):
    """Mock the get_all_resources"""
    monkeypatch.setattr(
        "mqss_client.MQSSClient.get_all_resources", MockMQSSClient.get_all_resources
    )
