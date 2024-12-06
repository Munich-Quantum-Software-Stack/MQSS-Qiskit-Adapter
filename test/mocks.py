"""Mock class for MQPClient"""

from typing import Dict, Optional

from mqp_client import ResourceInfo  # type: ignore


class MockMQPClient:
    """Mock MQPClient class"""

    def get_resource_info(self, name: str) -> Optional[ResourceInfo]:
        """Return the resource info"""
        if name == "res_cmap":
            return get_resource_info_cmap()
        if name == "res_no_cmap":
            return get_resource_info_no_cmap()
        if name == "res_offline":
            return get_resource_info_offline()
        return None

    def resources(self) -> Optional[Dict[str, ResourceInfo]]:
        """Return the resources"""
        # return get_resource_info_cmap() as dict to simulate the response from the server

        return {
            get_resource_info_cmap().name: get_resource_info_cmap(),
            get_resource_info_no_cmap().name: get_resource_info_no_cmap(),
            get_resource_info_offline().name: get_resource_info_offline(),
        }


def get_resource_info_cmap() -> ResourceInfo:
    """Return the resource info"""
    return ResourceInfo(
        name="res_cmap",
        qubits=5,
        online=True,
        connectivity=[[0, 2], [2, 0], [1, 2], [2, 1], [2, 3], [3, 2], [2, 4], [4, 2]],
        instructions=[
            ("r", {(0,): None, (1,): None, (2,): None, (3,): None, (4,): None}),
            ("id", {(0,): None, (1,): None, (2,): None, (3,): None, (4,): None}),
            (
                "cz",
                {
                    (0, 2): None,
                    (2, 0): None,
                    (1, 2): None,
                    (2, 1): None,
                    (2, 3): None,
                    (3, 2): None,
                    (2, 4): None,
                    (4, 2): None,
                },
            ),
            ("measure", {(0,): None, (1,): None, (2,): None, (3,): None, (4,): None}),
        ],
    )


def get_resource_info_no_cmap() -> ResourceInfo:
    """Return the resource info"""
    return ResourceInfo(
        name="res_no_cmap",
        qubits=5,
        online=True,
        connectivity=None,
        instructions=None,
    )


def get_resource_info_offline() -> ResourceInfo:
    """Return the resource info"""
    return ResourceInfo(
        name="res_offline",
        qubits=5,
        online=False,
        connectivity=None,
        instructions=None,
    )
