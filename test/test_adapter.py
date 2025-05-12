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

"""Module to test the MQSS Qiskit Adapter"""

import pytest
from mqss_client import MQSSClient  # type: ignore

from mqss.qiskit_adapter import MQSSQiskitBackend  # type: ignore

from .conftest import BACKENDS


class TestMQSSQiskitAdapter:
    """Test the MQSSQiskitAdapter"""

    @pytest.mark.backend
    def test_init(self, mqss_adapter):
        """Test the MQSSQiskitAdapter"""
        assert mqss_adapter.client is not None
        assert isinstance(mqss_adapter.client, MQSSClient)

    @pytest.mark.backend
    def test_get_backend(self, mqss_adapter):
        """Test the MQSSQiskitAdapter get_backend the default nameless backend"""
        backend = mqss_adapter.get_backend()
        assert isinstance(backend, MQSSQiskitBackend)
        assert backend.name is None
        assert backend.client is not None
        assert isinstance(backend.client, MQSSClient)

    @pytest.mark.backend
    def test_get_backend_name(self, mqss_adapter):
        """Test the MQSSQiskitAdapter get_backend by name"""
        for backend_name in BACKENDS:
            backend = mqss_adapter.get_backend(name=backend_name)
            assert isinstance(backend, MQSSQiskitBackend)
            assert backend.name == backend_name
            assert backend.client is not None
            assert isinstance(backend.client, MQSSClient)

    @pytest.mark.backend
    def test_get_backend_name_invalid(self, mqss_adapter):
        """Test the MQSSQiskitAdapter get_backend by invalid name"""
        with pytest.raises(ValueError):
            # This should raise an error since the backend name is invalid
            # and the backend is not available.
            mqss_adapter.get_backend(name="invalid_backend_name")

    @pytest.mark.backend
    def test_backends_name(self, mqss_adapter):
        """Test the MQSSQiskitAdapter backends by name"""
        for backend_name in BACKENDS:
            [backend] = mqss_adapter.backends(name=backend_name)
            assert isinstance(backend, MQSSQiskitBackend)
            assert backend.name == backend_name
            assert backend.client is not None
            assert isinstance(backend.client, MQSSClient)

    @pytest.mark.backend
    def test_backends_all(self, mqss_adapter):
        """Test the MQSSQiskitAdapter backends for all backends"""
        backends = mqss_adapter.backends()
        for backend in backends:
            assert isinstance(backend, MQSSQiskitBackend)
            assert backend.client is not None
            assert isinstance(backend.client, MQSSClient)

    @pytest.mark.backend
    def test_backends_online(self, mqss_adapter):
        """Test the MQSSQiskitAdapter backends"""
        backends = mqss_adapter.backends(online=True)
        for backend in backends:
            assert isinstance(backend, MQSSQiskitBackend)
            assert backend.client is not None
            assert isinstance(backend.client, MQSSClient)

    @pytest.mark.backend
    def test_backends_offline(self, mqss_adapter):
        """Test the MQSSQiskitAdapter backends"""
        backends = mqss_adapter.backends(online=False)
        for backend in backends:
            assert isinstance(backend, MQSSQiskitBackend)
            assert backend.client is not None
            assert isinstance(backend.client, MQSSClient)

    @pytest.mark.backend
    def test_backends_name_invalid(self, mqss_adapter):
        """Test the MQSSQiskitAdapter backends by name"""
        # This should raise an error since the backend name is invalid
        with pytest.raises(ValueError):
            mqss_adapter.backends(name="invalid_backend_name")
