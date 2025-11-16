"""Collision handling hooks for sprint/dash interactions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .game_state import GameState


class Target(Protocol):
    def apply_knockback(self, magnitude: float) -> None:
        ...

    def apply_infection(self, amount: float) -> None:
        ...


@dataclass
class CollisionHandler:
    game_state: GameState

    def on_collision(self, target: Target, *, sprinting: bool) -> None:
        config = self.game_state.flash_meter.config
        if sprinting:
            target.apply_knockback(config.knockback_force)
            target.apply_infection(config.infection_bonus)
            self.game_state.apply_knockback(config.knockback_force)
            self.game_state.apply_infection(config.infection_bonus)
            self.game_state.flash_meter.force_cooldown()
