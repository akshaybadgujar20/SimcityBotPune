# SimCity BuildIt Bot — Documentation

This documentation explains the **SimcityBotPune** bot: a Python automation system that controls SimCity BuildIt running on Android emulators via ADB. The bot automates repetitive in-game tasks—buying on Global Trade HQ, selling from the trade depot, collecting factories, and filling production queues—triggered either through a Flask REST API ([`simcity/bot/server.py`](../simcity/bot/server.py)) or standalone scripts.

## Suggested reading order

1. [Overview](overview.md) — what the bot does and how the package is organized
2. [API](api.md) — Flask endpoints, request schema, action dispatch
2.5. [Action guides](actions/README.md) — per-action functional understanding (when to use, flows, gaps)
3. [Architecture](architecture.md) — layers, concurrency, shared state
4. [City actions](city-actions.md) — high-level game task orchestration
5. [Automation](automation.md) — low-level ADB, CV, OCR primitives
6. [Data and enums](data-and-enums.md) — `MaterialInfo`, enums, JSON resources
7. [Trade bot](trade-bot.md) — refactored multi-item buyer subsystem
8. [Setup](setup.md) — prerequisites, install, running the server and trade_bot
9. [Legacy modules](legacy-modules.md) — experimental and superseded scripts

## Documentation index

| Document | Primary source directories |
|----------|---------------------------|
| [overview.md](overview.md) | [`simcity/bot/`](../simcity/bot/) (package root) |
| [api.md](api.md) | [`simcity/bot/server.py`](../simcity/bot/server.py) |
| [architecture.md](architecture.md) | [`server.py`](../simcity/bot/server.py), [`main.py`](../simcity/bot/main.py), [`city_actions/`](../simcity/bot/city_actions/), [`automation/`](../simcity/bot/automation/) |
| [city-actions.md](city-actions.md) | [`simcity/bot/city_actions/`](../simcity/bot/city_actions/) |
| [automation.md](automation.md) | [`simcity/bot/automation/`](../simcity/bot/automation/) |
| [data-and-enums.md](data-and-enums.md) | [`material_info.py`](../simcity/bot/material_info.py), [`enums/`](../simcity/bot/enums/), [`resources/material_data/`](../resources/material_data/) |
| [trade-bot.md](trade-bot.md) | [`simcity/bot/trade_bot/`](../simcity/bot/trade_bot/) |
| [setup.md](setup.md) | [`requirements.txt`](../requirements.txt), [`main.py`](../simcity/bot/main.py) |
| [legacy-modules.md](legacy-modules.md) | [`base/`](../simcity/bot/base/), [`cities/`](../simcity/bot/cities/), [`hotspot/`](../simcity/bot/hotspot/), [`test/`](../simcity/bot/test/) |
| [actions/README.md](actions/README.md) | [`server.py`](../simcity/bot/server.py) `perform_action` dispatch |

## Action guides

Per-action functional understanding documents for each `POST /action-perform` handler:

| Action | Guide |
|--------|-------|
| `CONTINUOUS_BUY` | [continuous-buy.md](actions/continuous-buy.md) |
| `SELL_WITH_FULL_VALUE` | [sell-with-full-value.md](actions/sell-with-full-value.md) |
| `SELL_WITH_ZERO_VALUE` | [sell-with-zero-value.md](actions/sell-with-zero-value.md) |
| `COLLECT_FROM_FACTORY` | [collect-from-factory.md](actions/collect-from-factory.md) |
| `ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION` | [add-commercial-to-production.md](actions/add-commercial-to-production.md) |
| `ADD_RAW_MATERIAL_TO_PRODUCTION` | [add-raw-to-production.md](actions/add-raw-to-production.md) |
| `ADVERTISE_ITEM_ON_TRADE_DEPOT` | [advertise-on-trade-depot.md](actions/advertise-on-trade-depot.md) |

Shared infrastructure (threading, stop, request fields): [actions/README.md](actions/README.md).

## Quick reference

- **API entry point:** `python simcity/bot/server.py` → `http://127.0.0.1:5000`
- **Device identity:** ADB TCP port string (e.g. `"5555"` → `127.0.0.1:5555`)
- **Production actions:** see [API action dispatch table](api.md#action-dispatch)
- **Logs:** `simcity_buildit.log` in the working directory
