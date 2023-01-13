# -*- coding: utf-8 -*-
"""Rules module.

This module provides rules management and useful dataclasses to
represent Rule and it's state.

Examples:
    Init new Rule::

        >>> from rules import RuleABC, pass_rules
        >>> chain = (RuleABC(), RuleABC())
        >>> await pass_rules("example string", chain)
            None

Attributes:
    QUAKE (str): Quake gametype
    WALLS (str): Walls gametype
    PAINTBALL (str): Paintball gametype
    SURVIVAL_GAMES (str): Survival Games gametype
    TNT_GAMES (str): TNT Games gametype
    VAMPIREZ (str): VampireZ gametype
    MEGA_WALLS (str): Mega Walls gametype
    ARCADE (str): Arcade gametype
    ARENA (str): Arena gametype
    UHC (str): UHC gametype
    COPS_AND_CRIMS (str): Cops & Crims gametype
    WARLORDS (str): Warlords gametype
    SMASH_HEROES (str): Smash Heroes gametype
    TURBO_KART_RACERS (str): Turbo Kart Racers gametype
    HOUSING (str): Housing gametype
    SKYWARS (str): Skywars gametype
    CRAZY_WALLS (str): Crazy Walls gametype
    SPEED_UHC (str): Speed UHC gametype
    SKYCLASH (str): Sky Clash gametype
    CLASSIC_GAMES (str): Legacy (Classic Games) gametype
    PROTOTYPE (str): Prototype gametype
    BEDWARS (str): BedWars gametype
    MURDER_MYSTERY (str): Murder Mystery gametype
    BUILD_BATTLE (str): Build Battle gametype
    DUELS (str): Duels gametype
    SKYBLOCK (str): Skyblock gametype
    PIT (str): The Pit gametype
    REPLAY (str): Replay (Viewing replay) gametype
    SMP (str): Hypixel SMP gametype

"""

from dataclasses import dataclass
from typing import Iterable, Optional

__all__ = (
    "RuleABC",
    "pass_rules"
)

QUAKE: str = "QUAKECRAFT"
WALLS: str = "WALLS"
PAINTBALL: str = "PAINTBALL"
SURVIVAL_GAMES: str = "SURVIVAL_GAMES"
TNT_GAMES: str = "TNTGAMES"
VAMPIREZ: str = "VAMPIREZ"
MEGA_WALLS: str = "WALLS3"
ARCADE: str = "ARCADE"
ARENA: str = "ARENA"
UHC: str = "UHC"
COPS_AND_CRIMS: str = "MCGO"
WARLORDS: str = "BATTLEGROUND"
SMASH_HEROES: str = "SUPER_SMASH"
TURBO_KART_RACERS: str = "GINGERBREAD" # What? Why?
HOUSING: str = "HOUSING"
SKYWARS: str = "SKYWARS"
CRAZY_WALLS: str = "TRUE_COMBAT" # What?! Why?!
SPEED_UHC: str = "SPEED_UHC"
SKYCLASH: str = "SKYCLASH"
CLASSIC_GAMES: str = "LEGACY"
PROTOTYPE: str = "PROTOTYPE"
BEDWARS: str = "BEDWARS"
MURDER_MYSTERY: str = "MURDER_MYSTERY"
BUILD_BATTLE: str = "BUILD_BATTLE"
DUELS: str = "DUELS"
SKYBLOCK: str = "SKYBLOCK"
PIT: str = "PIT"
REPLAY: str = "REPLAY"
SMP: str = "SMP"


@dataclass(frozen=True, slots=True)
class RuleABC:
    """Rule base class.

    Rules are used to determine when notification should be
    sent to Discord webhook.

    Attributes:
        message_format (str): Notification message format

    """

    message_format: str

    def consume(self, status) -> Optional[str]:
        """Consumes status and checks it.

        Args:
            status (:obj:`StatusABC`): Status

        Returns:
            str: Message content if status passes, otherwise None

        """
        pass


@dataclass(frozen=True, slots=True)
class GameRule(RuleABC):
    """Rule that checks for all game fields.

    Checks for players online status, gametype, game mode, game map.

    Attributes:
        gametype (str): Gametype
        game_mode (str): Game mode
        game_map (str): Game map

    """

    online: bool
    gametype: str = None
    game_mode: str = None
    game_map: str = None

    def consume(self, status) -> Optional[str]:
        """Consumes status and checks it.

        Args:
            status (:obj:`StatusABC`): Status

        Returns:
            str: Message content if status passes, otherwise None

        """
        online: bool = self.online == status.online
        gametype: bool = (not self.gametype) or self.gametype == status.gameType
        gamemode: bool = (not self.game_mode) or self.game_mode == status.mode
        gamemap: bool = (not self.game_map) or self.game_map == status.map

        return self.message_format.format(uuid=status.uuid, gametype=status.gameType, mode=status.mode, map=status.map) if \
                    (online and gametype and gamemode and gamemap) else None


async def pass_rules(status, rules: Iterable[RuleABC]) -> Optional[str]:
    """Passes ``Status`` object through rules list.

    Applies every rule for ``Status`` object until one passes.

    Args:
        status (:obj:`StatusABC`): Status
        rules (iterable): Rules iterable

    Returns:
        str: Message content if status passes rule, otherwise None

    """
    for rule in rules:

        # If rule passes, return message
        if message := rule.consume(status):
            return message
