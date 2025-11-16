"""Flash meter state container and events."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

EventHook = Callable[[str, Dict[str, float]], None]


@dataclass
class FlashMeterConfig:
    max_meter: float
    recharge_rate: float
    dash_cost: float
    cooldown: float
    sprint_recharge_multiplier: float = 0.0
    knockback_force: float = 0.0
    infection_bonus: float = 0.0


@dataclass
class FlashMeterState:
    """Owns meter value, timers, and exposes event hooks."""

    config: FlashMeterConfig
    current_meter: float = field(init=False)
    cooldown_remaining: float = field(default=0.0, init=False)
    event_hooks: List[EventHook] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.current_meter = self.config.max_meter

    def register_event_hook(self, hook: EventHook) -> None:
        self.event_hooks.append(hook)

    def _emit(self, event: str, payload: Optional[Dict[str, float]] = None) -> None:
        if payload is None:
            payload = {}
        for hook in self.event_hooks:
            hook(event, payload)

    def tick(self, delta_time: float, *, sprinting: bool = False) -> None:
        if delta_time <= 0:
            return
        if self.cooldown_remaining > 0:
            self.cooldown_remaining = max(0.0, self.cooldown_remaining - delta_time)
            if self.cooldown_remaining == 0:
                self._emit("cooldown_complete")
        recharge = self.config.recharge_rate * delta_time
        if sprinting:
            recharge *= 1.0 + self.config.sprint_recharge_multiplier
        prev = self.current_meter
        self.current_meter = min(self.config.max_meter, self.current_meter + recharge)
        if int(prev) != int(self.current_meter):
            self._emit("meter_change", {"value": self.current_meter})

    def can_dash(self) -> bool:
        return self.current_meter >= self.config.dash_cost and self.cooldown_remaining == 0

    def spend_for_dash(self) -> bool:
        if not self.can_dash():
            self._emit("dash_denied", {"value": self.current_meter})
            return False
        self.current_meter -= self.config.dash_cost
        self.cooldown_remaining = self.config.cooldown
        self._emit("dash", {"value": self.current_meter})
        self._emit("cooldown_start", {"remaining": self.cooldown_remaining})
        return True

    def force_cooldown(self, cooldown: Optional[float] = None) -> None:
        self.cooldown_remaining = cooldown if cooldown is not None else self.config.cooldown
        self._emit("cooldown_start", {"remaining": self.cooldown_remaining})
