# -*- coding: utf-8 -*-
"""Main configuration module.

This module should be used only for configuration.

Attributes:
    webhook_url (str): Discord WebHook URL.
    hypixel_token (str): Hypixel API token. Can be obtained
        by joining Hypixel and typing ``/api``
"""

from typing import Tuple

from hypixelguard.rules import SKYBLOCK, GameRule

webhook_url: str = "<webhook>"
hypixel_token: str = "<token>"

# Strictly ordered
uuids: Tuple[str] = (
    "<player-uuid>",
    "<player-uuid>",
)

# Strictly ordered
rules: tuple = (
    GameRule(message_format="SKYBLOCK: {uuid} got onto Private Island", online=True,
             gametype=SKYBLOCK, game_mode="dynamic"),
    GameRule(message_format="SKYBLOCK: {uuid} warped to {mode} - {map}!", online=True,
             gametype=SKYBLOCK),
    GameRule(message_format="{uuid} joined Hypixel!", online=True), # Fallback
    GameRule(message_format="{uuid} left Hypixel!", online=False),  # Fallback
)
