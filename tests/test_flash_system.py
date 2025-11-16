from zombie_flash.game_state import GameState
from zombie_flash.player_controller import PlayerController
from zombie_flash.collision import CollisionHandler
from ui.cooldown_display import CooldownDisplay


class DummyTarget:
    def __init__(self) -> None:
        self.knockback = 0.0
        self.infection = 0.0

    def apply_knockback(self, magnitude: float) -> None:
        self.knockback += magnitude

    def apply_infection(self, amount: float) -> None:
        self.infection += amount


def test_dash_consumes_meter_and_emits_fx():
    state = GameState()
    fx_events = []

    def fx_hook(event: str) -> None:
        fx_events.append(event)

    controller = PlayerController(state, fx_hook=fx_hook)
    assert controller.handle_direction("forward", 0.1) is False
    assert controller.handle_direction("forward", 0.2) is True
    assert "dash_start" in fx_events
    assert state.flash_meter.current_meter == state.flash_meter.config.max_meter - state.flash_meter.config.dash_cost


def test_collision_knockback_and_infection():
    state = GameState()
    handler = CollisionHandler(state)
    target = DummyTarget()
    handler.on_collision(target, sprinting=True)
    assert target.knockback == state.flash_meter.config.knockback_force
    assert target.infection == state.flash_meter.config.infection_bonus
    assert state.telemetry["infection_delta"] == state.flash_meter.config.infection_bonus


def test_cooldown_display_updates():
    state = GameState()
    display = CooldownDisplay(state.flash_meter)
    state.flash_meter.force_cooldown(0.5)
    assert display.normalized_value == 1.0
    state.tick(0.5)
    assert display.normalized_value == 0.0
