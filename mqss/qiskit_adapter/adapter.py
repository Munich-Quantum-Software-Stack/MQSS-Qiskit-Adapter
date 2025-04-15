"""MQSS Qiskit Adapter"""

import os
from typing import List, Optional

from mqss_client import MQSSClient  # type: ignore

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
        hpcqc: Optional[bool] = None,
        base_url: Optional[str] = None,
    ) -> None:
        is_hpcqc_env = os.getenv("MQSS_HPCQC_ENV", "False").lower() in [
            "true",
            "1",
            "t",
        ]
        # hpcqc gets priority over the environment variable
        self.client = MQSSClient(
            token=token,
            base_url=base_url,
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
        self, name: Optional[str] = None, online_backends: bool = False, **kwargs
    ) -> List[MQSSQiskitBackend]:
        """Return a list of all available backends

        Args:
            name (Optional[str]): name of the backend to return
            online_backends (bool): return only online backends

        Returns:
            List[MQSSQiskitBackend]: List of backend instances
        """
        resources = self.client.get_all_resources()
        if resources is None:
            return []
        return [
            MQSSQiskitBackend(self.client, _name, resources[_name])
            for _name in resources
            if (not online_backends or resources[_name].online)
            and (name is None or name == _name)
        ]
