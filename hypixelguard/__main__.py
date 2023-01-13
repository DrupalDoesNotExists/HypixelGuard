# -*- coding: utf-8 -*-
"""Program entry point.

This module runs the discord bot and Hypixel API checker. Should be
only EXECUTED, not IMPORTED!

Example:
    You can run this entire module this way::

        $ python -m HypixelGuard

Todo:
    * Basic features
    * Advanced configuration

.. Original Hypixel thread:
    https://hypixel.net/threads/writing-a-discord-bot-to-run-24-7.5232684/#post-37518402

.. Google documentation style:
    http://google.github.io/styleguide/pyguide.html

"""

import asyncio as aio
from typing import Dict, Optional
from logging import basicConfig, getLogger, Logger, INFO

from settings import uuids, rules

from .hypixel import StatusABC, get_status, validate_token
from .rules import pass_rules
from .webhook import send_message


# Logger variable
basicConfig(level=INFO)
_logger: Logger = getLogger()


async def update_api_state() -> None:
    """Updates Hypixel API state from remote.

    Makes GET requests for specified in settings UUIDs.
    """

    # Validate API token
    _logger.info("Validating API token")

    if status_code := (await validate_token()) != 200:
        _logger.warning(f"Token validation failed with response code {status_code}")
        return

    # Registry for status snapshots
    registry: Dict[str, StatusABC] = {}

    _logger.info("Running API state updating loop")
    while True:

        for uuid in uuids:
            snapshot: StatusABC = registry.get(uuid)
            current: StatusABC = await get_status(uuid=uuid)

            # Update cached state
            registry[uuid] = current

            if snapshot != current:
                # Are current state different with cached snapshot?
                message: Optional[str] = await pass_rules(status=current, rules=rules)
                if message:
                    await send_message(content=message, username=uuid)

        # Wait a minute
        await aio.sleep(60)


aio.run(update_api_state())
