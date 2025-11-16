# Zombie Flash Prototype

This repository sketches out a meter-driven dash/Flash loop. Highlights:

1. **Centralized Flash meter** — `GameState` hosts `FlashMeterState`, exposing event hooks and timers for recharge/cooldown, plus `PlayerStats` for infection bonuses.
2. **Dash input** — `PlayerController` supports double-tap detection or dedicated dash input, spends meter, and fires FX hooks.
3. **Collision handling** — `CollisionHandler` applies knockback/infection bonuses while sprinting and forces cooldown; `CooldownDisplay` mirrors cooldown UI feedback.
4. **Data-driven tuning** — `data/flash_meter.json` stores max meter, cost, recharge rate, sprint bonuses, and knockback/infection values for quick iteration.

Run the tests with `pytest` to exercise the flow end-to-end.
