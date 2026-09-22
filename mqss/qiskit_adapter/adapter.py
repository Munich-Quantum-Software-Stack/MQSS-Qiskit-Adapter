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

"""MQSS Qiskit Adapter"""

import os
from typing import List, Optional

from mqss.client import MQSSClient  # type: ignore

from .backend import MQSSQiskitBackend


class MQSSQiskitAdapter:
    """MQSSQiskitAdapter allows users to access MQSS Qiskit backends.

    Args:
        token (str): MQP token
        hpcqc (bool): Enable offloading task directly from HPC node to MQSS backend
        base_url (str): MQSS endpoint
    """

    def __init__(
        self,
        token: str,
        *,
        hpcqc: Optional[bool] = False,
        base_url: Optional[str] = "",
    ) -> None:
        is_hpcqc_env = os.getenv("MQSS_HPCQC_ENV", "False").lower() in [
            "true",
            "1",
            "t",
        ]
        # hpcqc gets priority over the environment variable

        self.client = MQSSClient(
            token=token,
            url_or_queue=base_url,
            is_hpc=hpcqc if hpcqc is not None else is_hpcqc_env,
        )

    def get_backend(self, name: Optional[str] = None, **kwargs) -> MQSSQiskitBackend:
        """Return a backend by name

        Args:
            name (Optional[str]): name of the backend

        Returns:
            A backend instance
        """

        return MQSSQiskitBackend(self.client, name, **kwargs)

    def backends(
        self, *, name: Optional[str] = None, online: bool = False, **kwargs
    ) -> List[MQSSQiskitBackend]:
        """Return a list of all available backends

        Args:
            name (Optional[str]): name of the backend to return
            online (bool): return only online backends

        Returns:
            List[MQSSQiskitBackend]: List of backend instances
        """
        resources = self.client.resources
        if resources is None:
            return []
        if name is not None and not any(
            [name == resource.name for resource in resources]
        ):
            raise ValueError(f"{name} is not available. ")
        return [
            MQSSQiskitBackend(self.client, resource.name, resource)
            for resource in resources
            if (not online or resource.online)
            and (name is None or name == resource.name)
        ]
