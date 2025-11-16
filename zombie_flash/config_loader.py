"""Load flash meter config from data tables."""
from __future__ import annotations

import json
from pathlib import Path

from .flash_meter import FlashMeterConfig

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "flash_meter.json"


def load_flash_meter_config(path: Path = DATA_PATH) -> FlashMeterConfig:
    data = json.loads(path.read_text())
    return FlashMeterConfig(
        max_meter=float(data["maxMeter"]),
        recharge_rate=float(data["baseRechargeRate"]),
        dash_cost=float(data["dashCost"]),
        cooldown=float(data["cooldownSeconds"]),
        sprint_recharge_multiplier=float(data.get("sprintRechargeMultiplier", 0.0)),
        knockback_force=float(data.get("knockbackForce", 0.0)),
        infection_bonus=float(data.get("infectionBonus", 0.0)),
    )
