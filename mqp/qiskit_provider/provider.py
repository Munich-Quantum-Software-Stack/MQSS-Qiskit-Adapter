"""MQP Qiskit Provider"""

from typing import List, Optional
from warnings import warn

from mqp_client import MQPClient  # type: ignore
from qiskit.providers import ProviderV1  # type: ignore

from .backend import MQPBackend


class MQPProvider(ProviderV1):
    """MQP Qiskit Provider Class

    Args:
        token (str): MQP token
        url (str, optional): MQP URL
    """

    def __init__(self, token: str, url: Optional[str] = None) -> None:
        if url:
            self._client = MQPClient(url=url, token=token)

        else:
            self._client = MQPClient(token=token)

    def get_backend(self, name=None, **kwargs) -> MQPBackend:
        """Return a backend by name (deprecated since Qiskit v1.1, use backends instead)

        Args:
            name (str): name of the backend

        Returns:
            MQPBackend: backend instance
        """

        warn(
            "get_backend is deprecated since Qiskit v1.1, use backends instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return MQPBackend(name, self._client, **kwargs)

    def backends(self, name=None, online_backends=False, **kwargs) -> List[MQPBackend]:
        """Return a list of available backends

        Args:
            name (str): name of the backend to return
            online_backends (bool): return only online backends (default: False)

        Returns:
            list[MQPBackend]: list of backend instances
        """
        resources = self._client.resources()
        if resources is None:
            return []
        return [
            MQPBackend(_name, self._client, resources[_name])
            for _name in resources
            if (not online_backends or resources[_name].online)
            and (name is None or name == _name)
        ]
