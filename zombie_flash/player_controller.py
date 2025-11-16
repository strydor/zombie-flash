"""Player controller with dash input and FX hooks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from .game_state import GameState

DashFXHook = Callable[[str], None]


@dataclass
class DashInputState:
    double_tap_window: float = 0.25
    last_direction: Optional[str] = None
    last_time: float = 0.0

    def register_input(self, direction: str, timestamp: float) -> bool:
        if self.last_direction == direction and timestamp - self.last_time <= self.double_tap_window:
            self.last_direction = None
            return True
        self.last_direction = direction
        self.last_time = timestamp
        return False


class PlayerController:
    def __init__(self, game_state: GameState, fx_hook: Optional[DashFXHook] = None) -> None:
        self.state = game_state
        self.fx_hook = fx_hook
        self.input_state = DashInputState()
        self.dashing: bool = False
        self.dash_direction: Optional[str] = None

    def _trigger_fx(self, cue: str) -> None:
        if self.fx_hook:
            self.fx_hook(cue)

    def handle_direction(self, direction: str, timestamp: float, *, dedicated_dash: bool = False) -> bool:
        triggered = dedicated_dash or self.input_state.register_input(direction, timestamp)
        if not triggered:
            return False
        if not self.state.flash_meter.spend_for_dash():
            self._trigger_fx("dash_denied")
            return False
        self.dashing = True
        self.dash_direction = direction
        self._trigger_fx("dash_start")
        return True

    def end_dash(self) -> None:
        if self.dashing:
            self.dashing = False
            self._trigger_fx("dash_end")

    def tick(self, delta_time: float, *, sprinting: bool = False) -> None:
        self.state.tick(delta_time, sprinting=sprinting)
        if self.dashing and self.state.flash_meter.cooldown_remaining == 0:
            self.end_dash()
