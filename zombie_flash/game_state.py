"""Game state container for flash meter and player stats."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .config_loader import load_flash_meter_config
from .flash_meter import FlashMeterState


@dataclass
class PlayerStats:
    health: float = 100.0
    infection: float = 0.0
    speed_multiplier: float = 1.0

    def apply_infection(self, amount: float) -> None:
        self.infection = min(1.0, self.infection + amount)


class GameState:
    def __init__(self) -> None:
        self.player_stats = PlayerStats()
        config = load_flash_meter_config()
        self.flash_meter = FlashMeterState(config)
        self.telemetry: Dict[str, float] = {}

        def _record(event: str, payload: Dict[str, float]) -> None:
            self.telemetry[event] = payload.get("value", payload.get("remaining", 0.0))

        self.flash_meter.register_event_hook(_record)

    def tick(self, delta_time: float, *, sprinting: bool = False) -> None:
        self.flash_meter.tick(delta_time, sprinting=sprinting)

    def apply_knockback(self, magnitude: float) -> None:
        self.telemetry["knockback"] = magnitude

    def apply_infection(self, amount: float) -> None:
        before = self.player_stats.infection
        self.player_stats.apply_infection(amount)
        self.telemetry["infection_delta"] = self.player_stats.infection - before
