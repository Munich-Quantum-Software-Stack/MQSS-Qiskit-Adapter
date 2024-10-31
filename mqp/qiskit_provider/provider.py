"""MQP Qiskit Provider"""

from typing import Optional

from mqp_client import MQPClient  # type: ignore
from qiskit.providers import ProviderV1  # type: ignore

from .backend import MQPBackend


class MQPProvider(ProviderV1):
    """MQP Qiskit Provider Class"""

    def __init__(self, token: str, url: Optional[str] = None) -> None:
        if url:
            self._client = MQPClient(url=url, token=token)

        else:
            self._client = MQPClient(token=token)

    def get_backend(self, name=None, **kwargs) -> MQPBackend:
        return MQPBackend(name, self._client, **kwargs)

    def backends(self, name=None, **kwargs):
        resources = self._client.resources()
        if resources is None:
            return []
        return [MQPBackend(name, self._client, resources[name]) for name in resources]
