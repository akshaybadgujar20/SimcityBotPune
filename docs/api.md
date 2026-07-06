# API Reference

[← Back to index](README.md)

The Flask server in [`simcity/bot/server.py`](../simcity/bot/server.py) exposes a small REST API on `127.0.0.1:5000`. It is the **primary production entry point** for triggering game automation on Android emulators.

## Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Welcome / health check |
| `/action-perform` | POST | Start a city action on a given emulator port |
| `/action-stop` | POST | Request stop for the action running on a port |

CORS is enabled for all origins (`flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})`).

## `GET /`

Returns a JSON welcome message:

```json
{"message": "Welcome to the Flask API!"}
```

## `POST /action-perform`

Starts a background thread that runs a city action function.

### Request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `port` | string | Yes | ADB TCP port of the emulator (e.g. `"5555"`) |
| `action` | string | Yes | Action identifier (see [action dispatch](#action-dispatch)) |
| `selectedMaterials` | string[] | No | Material enum names in priority order (e.g. `["STORAGE_BARS", "STORAGE_LOCK"]`) |
| `factoriesCount` | number | No | Number of factories for factory-related actions |

Example:

```json
{
  "port": "5555",
  "action": "CONTINUOUS_BUY",
  "selectedMaterials": ["STORAGE_BARS"],
  "factoriesCount": 12
}
```

### Processing flow

1. `load_material_info_data()` loads or returns cached `MaterialInfo` objects.
2. `set_up(city_port)` configures logging and connects ADB to `127.0.0.1:{port}`.
3. If `selectedMaterials` is non-empty, each name is resolved to a `MaterialInfo` and a priority map is built (`Material[name] → index + 1`). **Note:** priorities are computed but not passed to most handlers today.
4. The `action` string selects a handler; `start_action(city_port, handler, args)` spawns a daemon thread.
5. Returns `{"message": "action started"}` with HTTP 200.

Unknown actions return `{"message": "unknown action"}` with HTTP 200.

### Action dispatch

| `action` value | Handler | Arguments passed | Functional guide | Notes |
|----------------|---------|------------------|------------------|-------|
| `CONTINUOUS_BUY` | `run_trade_session` | `(city_port, purchase_items)` | [continuous-buy](actions/continuous-buy.md) | **All** `selectedMaterials`; empty list → HTTP 400 |
| `SELL_WITH_FULL_VALUE` | `sell_materials` | `(select_material_list, city_port, False, True)` | [sell-with-full-value](actions/sell-with-full-value.md) | `advertise=False`, `full_price=True` |
| `SELL_WITH_ZERO_VALUE` | `sell_materials` | `(select_material_list, city_port, False, False)` | [sell-with-zero-value](actions/sell-with-zero-value.md) | `advertise=False`, `full_price=False` |
| `COLLECT_FROM_FACTORY` | `collect_raw_materials` | `(factoriesCount, city_port)` | [collect-from-factory](actions/collect-from-factory.md) | |
| `ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION` | `add_commercial_material_to_production` | `(select_material_list, city_port)` | [add-commercial-to-production](actions/add-commercial-to-production.md) | All selected materials |
| `ADD_RAW_MATERIAL_TO_PRODUCTION` | `add_raw_material_to_production` | `(select_material_list[0], factoriesCount, city_port)` | [add-raw-to-production](actions/add-raw-to-production.md) | First material only |
| `ADVERTISE_ITEM_ON_TRADE_DEPOT` | *(none)* | — | [advertise-on-trade-depot](actions/advertise-on-trade-depot.md) | Prints `no action mapped`; **not implemented** |

Action string constants align with [`enums/city_actions.py`](../simcity/bot/enums/city_actions.py) enum names (without the human-readable values).

For in-game behavior of each handler, see [city-actions.md](city-actions.md) or the per-action [functional guides](actions/README.md).

### Example requests

Start continuous buy on port 5555:

```bash
curl -X POST http://127.0.0.1:5000/action-perform \
  -H "Content-Type: application/json" \
  -d "{\"port\": \"5555\", \"action\": \"CONTINUOUS_BUY\", \"selectedMaterials\": [\"STORAGE_BARS\"], \"factoriesCount\": 12}"
```

Sell materials at full price:

```bash
curl -X POST http://127.0.0.1:5000/action-perform \
  -H "Content-Type: application/json" \
  -d "{\"port\": \"5555\", \"action\": \"SELL_WITH_FULL_VALUE\", \"selectedMaterials\": [\"STORAGE_BARS\", \"STORAGE_LOCK\"], \"factoriesCount\": 0}"
```

Collect from 12 factories:

```bash
curl -X POST http://127.0.0.1:5000/action-perform \
  -H "Content-Type: application/json" \
  -d "{\"port\": \"5555\", \"action\": \"COLLECT_FROM_FACTORY\", \"selectedMaterials\": [], \"factoriesCount\": 12}"
```

## `POST /action-stop`

Signals the running action on a port to stop by setting its `threading.Event`.

### Request body

```json
{
  "port": "5555"
}
```

### Responses

| Condition | Response | HTTP |
|-----------|----------|------|
| Port has a registered stop event | `{"message": "action stop requested"}` | 200 |
| No running action for port | `{"message": "no running action for this city"}` | 200 |

Stop is **cooperative** — city actions must check `stop_event.is_set()` in their loops. Not all actions do (see [city-actions.md](city-actions.md)).

## Threading model

`start_action` in `server.py`:

```python
def start_action(city_port, target, args):
    if city_port in stop_events:
        stop_events[city_port].set()      # stop previous action

    stop_event = Event()
    stop_events[city_port] = stop_event

    thread = Thread(
        target=target,
        args=(*args, stop_event),         # stop_event always last arg
        daemon=True
    )
    running_actions[city_port] = thread
    thread.start()
```

Key behaviors:

- **One action per port** — starting a new action preempts the old one.
- **`stop_event` is always appended** as the last argument to city action functions.
- **In-memory only** — `running_actions` and `stop_events` are not persisted; server restart clears state.
- **Daemon threads** — do not prevent process exit.

## Actions not exposed via API

These `city_actions` modules exist but have **no** `/action-perform` mapping:

| Module | Suggested `CityAction` enum |
|--------|----------------------------|
| `collect_sold_item_money` | `COLLECT_SOLD_ITEM_MONEY` |
| `advertise_all_items_on_trade_depot` | `ADVERTISE_ITEM_ON_TRADE_DEPOT` |

The `trade_bot` subsystem is also not API-wired. See [trade-bot.md](trade-bot.md).

## Running the server

```bash
python simcity/bot/server.py
```

Binds to `127.0.0.1:5000` with `debug=False`. See [setup.md](setup.md) for prerequisites.

## Related documents

- [Architecture](architecture.md) — request lifecycle and concurrency
- [City actions](city-actions.md) — what each handler does in-game
- [Setup](setup.md) — emulator and dependency setup
