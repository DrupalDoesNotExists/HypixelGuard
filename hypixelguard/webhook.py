# -*- coding: utf-8 -*-
"""Discord webhook wrapper module.

This module performs various tasks with Discord webhooks and contains
useful ABC classes for object representation.

Examples:
    This API is async so You can't really run this from shell.

    Sending notification with webhook::

        >>> import webhook
        >>> from hypixel import get_status
        >>> await webhook.send_status(status=await get_status())

    Sending custom message::

        >>> import webhook
        >>> message: webhook.MessageABC = webhook.MessageABC(message="Custom message", name="Name", avatar=webhook.POSITIVE)
        >>> await webhook.send_message(message=message)

Raises:
    ValueError: If `webhook_url` is empty.

Todo:
    * Dataclasses
    * API methods

"""

from dataclasses import asdict, dataclass
from typing import Dict, Optional

from httpx import AsyncClient
from settings import webhook_url

from .hypixel import StatusABC

__all__ = (
    "MessageABC",
    "POSITIVE",
    "NEGATIVE",
    "PASSIVE",
    "send_message",
)


@dataclass(frozen=True, slots=True)
class MessageABC:
    """Message dataclass.

    Contains needed message information like content, avatar URL, username.

    Attributes:
        content (str): Message content.
        avatar_url (obj:`str`, optional): Avatar URL (override webhook default).
        username (obj:`str`, optional):  Username (override webhook default).

    """

    content: str
    avatar_url: Optional[str] = None
    username: Optional[str] = None


if not webhook_url:
    raise ValueError("Webhook URL is empty")

# Single (non-documented) internal client instance for all requests
_client: AsyncClient = AsyncClient()


async def send_message(message: Optional[MessageABC] = None, **kwargs) -> None:
    """Sends message via webhook.

    Sends ``MessageABC`` instance to webhook by HTTP Post.

    Args:
        message (:obj:`MessageABC`, optional): Message to send.
            You can also use kwargs and pass fields explicitly.
        **kwargs: Explicit fields.

    """

    # Construct Message object if no passed
    message: MessageABC = message if message else MessageABC(**kwargs)

    # Represent MessageABC as dict without None values
    json: Dict[str, object] = asdict(message, dict_factory=lambda values:
                                     {key: value for key, value in values if value})

    await _client.post(webhook_url, json=json)
