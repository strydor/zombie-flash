"""Simple cooldown feedback component."""
from __future__ import annotations

from dataclasses import dataclass

from zombie_flash.flash_meter import FlashMeterState


@dataclass
class CooldownDisplay:
    meter: FlashMeterState
    normalized_value: float = 0.0

    def __post_init__(self) -> None:
        self.meter.register_event_hook(self.on_event)

    def on_event(self, event: str, payload):
        if event == "cooldown_start":
            self.normalized_value = 1.0
        elif event == "cooldown_complete":
            self.normalized_value = 0.0
        elif event == "meter_change":
            self.normalized_value = self.meter.cooldown_remaining / max(1e-5, self.meter.config.cooldown)
