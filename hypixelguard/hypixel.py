# -*- coding: utf-8 -*-
"""Hypixel API wrapper module.

Does various checks with Hypixel API and contains useful ABC
classes for object representation.

Examples:
    This API is async so You can't really run this from shell.

    Validate token (returns status code)::

        >>> import hypixel
        >>> await hypixel.validate_token()
            200

    Get current player status::

        >>> import hypixel
        >>> await hypixel.get_status(uuid="<uuid>")
            StatusABC(uuid="<uuid>", online=True, gameType="Custom", mode="Custom", map="Custom")

Raises:
    ValueError: If `hypixel_token` is empty.

"""

from dataclasses import dataclass
from time import time
from typing import Dict, Optional

from httpx import AsyncClient, Response
from settings import hypixel_token

__all__ = (
    "StatusABC",
    "validate_token",
    "get_status",
)


@dataclass(frozen=True, slots=True)
class StatusABC:
    """Player status dataclass.

    Represents Player status snapshot at the single moment.
    Use ``get_status(uuid="<uuid>")`` to get newer object.

    Attributes:
        timestamp (float): Status creation timestamp.
        uuid (str): Player UUID.

    """

    uuid: str
    _internal_data: Dict[str, object]
    timestamp: float = time()

    @property
    def online(self) -> bool:
        """bool: True if player is online, otherwise False."""
        return self._internal_data['online']

    @property
    def gameType(self) -> Optional[str]:
        """str: Gametype of game player currently playing."""
        return self._internal_data.get("gameType")

    @property
    def mode(self) -> Optional[str]:
        """str: Game mode of game player currently playing."""
        return self._internal_data.get("mode")

    @property
    def map(self) -> Optional[str]:
        """str: Game map of game player currently playing on."""
        return self._internal_data.get("map")


if not hypixel_token:
    raise ValueError("Hypixel API token is empty.")

# Client instance
_client: AsyncClient = AsyncClient(headers={"API-Key": hypixel_token},
                                   base_url="https://api.hypixel.net")


async def validate_token() -> int:
    """Validates API token.

    Checks if token is valid with GET request to Hypixel API.

    Returns:
        int: Response status code

    Raises:
        ValueError: If response isn't successful

    """
    response: Response = await _client.get("/key")
    if response.is_error:
        raise ValueError(response.json())

    return response.status_code


async def get_status(uuid: str) -> StatusABC:
    """Gets player online status.

    Sends GET request to Hypixel API and get current players online status
    snapshot. Returned object is immutable and will not be updated.

    Args:
        uuid (str): Player UUID

    Returns:
        :obj:`Status`: Current online status snapshot

    Raises:
        ValueError: If request isn't successful

    """
    response: Response = await _client.get("/status", params={"uuid": uuid})
    json: dict = response.json()

    if response.is_error:
        raise ValueError(json)

    return StatusABC(uuid=uuid, _internal_data=json['session'])
