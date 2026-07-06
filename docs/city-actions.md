# City Actions

[← Back to index](README.md)

City actions are **high-level game workflows** in [`simcity/bot/city_actions/`](../simcity/bot/city_actions/). Each module orchestrates [`automation/`](automation.md) primitives to achieve an in-game outcome. The Flask server dispatches most of these via `POST /action-perform` — see [API](api.md).

Every API-dispatched function receives a final `stop_event: threading.Event` argument appended by `start_action()` in [`server.py`](../simcity/bot/server.py).

---

## `buy_items.py`

| | |
|---|---|
| **Purpose** | Continuously buy a single material from Global Trade HQ |
| **Server action** | `CONTINUOUS_BUY` |
| **Signature** | `buy_items(material_to_be_found, device_id, stop_event)` |

### Algorithm

1. Create HQ timer (`global_trade_hq_timer`).
2. Open purchase menu → Global Trade HQ.
3. Loop up to 1000 iterations:
   - Tap Best Value → reopen Global Trade HQ.
   - Wait for COIN icon (up to 15s) and start timer when HQ view is ready.
   - Search HQ view 1 for material via `find_material_in_global_trade_hq`.
   - If not found, swipe right and check views 2 and 3.
   - On match: `buy_item_from_visiting_city_trade_depot` → click listing, wait for visiting depot, `buy_item`.
   - On no match across views: `set_timer()` — sleep until ~30s refresh window elapses.

### Key automation calls

- [`click_on_purchase_menu`](../simcity/bot/automation/city_utility_actions.py), [`click_on_global_trade_hq`](../simcity/bot/automation/city_utility_actions.py), [`click_on_best_value_menu`](../simcity/bot/automation/city_utility_actions.py)
- [`find_miscellaneous_material`](../simcity/bot/automation/find_material.py) (`COIN`)
- [`find_material_in_global_trade_hq`](../simcity/bot/automation/find_material.py), [`find_material_in_trade_depot`](../simcity/bot/automation/find_material.py)

### Exported helpers (reused by `trade_bot`)

- `buy_item_from_visiting_city_trade_depot(material, found_item_list, device_id)` — click HQ listing, travel to mayor
- `buy_item(material, device_id)` — buy inside visiting depot, swipe pages if needed
- `set_timer()` — wait remainder of 30s HQ refresh period

### Stop behavior

**Does not check `stop_event`** in the main loop. Stop only takes effect if the thread is preempted by a new action on the same port.

---

## `sell_materials.py`

| | |
|---|---|
| **Purpose** | List materials from city storage into empty trade depot slots at full or zero price |
| **Server actions** | `SELL_WITH_FULL_VALUE`, `SELL_WITH_ZERO_VALUE` |
| **Signature** | `sell_materials(materials, device_id, advertise, full_price, stop_event, max_city_storage_scrolls=15, max_depot_pages=4)` |

### Algorithm

1. Open purchase menu → own trade depot.
2. Scan for empty trade boxes on current depot page.
3. For each material in the list:
   - Get next empty trade box (paginate depot up to `max_depot_pages`).
   - Open empty box → open correct storage (city storage for commercial, material storage for factory items).
   - Find material in storage (scroll up to `max_city_storage_scrolls` pages); OCR quantity via `capture_material_quantity`.
   - Sell in batches of up to 5 via `sell_material` until quantity exhausted or depot full.
   - Open additional empty boxes as needed for remaining quantity.

### Key automation calls

- [`find_miscellaneous_material`](../simcity/bot/automation/find_material.py) (`EMPTY_TRADE_BOXES`, `BUY_ICON`)
- [`find_material_in_city_storage`](../simcity/bot/automation/find_material.py)
- [`open_empty_trade_box`](../simcity/bot/automation/open_empty_trade_box.py), [`sell_material`](../simcity/bot/automation/sell_material.py)
- [`capture_material_quantity`](../simcity/bot/automation/find_empty_trade_boxes_and_sell_material.py)

### Stop behavior

Checks `stop_event.is_set()` at multiple points throughout the sell loop.

---

## `collect_raw_materials.py`

| | |
|---|---|
| **Purpose** | Tap factory collection slots to collect produced raw materials |
| **Server action** | `COLLECT_FROM_FACTORY` |
| **Signature** | `collect_raw_materials(no_of_factories, device_id, stop_event)` |

### Algorithm

1. Click factory navigation coordinate `(500, 140)`.
2. For each factory (1..`no_of_factories`):
   - Tap five collection slot coordinates in a row.
   - Re-click factory navigation to advance.

Uses **fixed screen coordinates** — not template matching.

### Stop behavior

Checks `stop_event` between factories.

---

## `add_raw_material_to_production.py`

| | |
|---|---|
| **Purpose** | Drag a raw material from storage into factory production slots |
| **Server action** | `ADD_RAW_MATERIAL_TO_PRODUCTION` |
| **Signature** | `add_raw_material_to_production(material, no_of_factories, device_id, stop_event)` |

### Algorithm

1. Click factory navigation `(500, 140)`.
2. For each factory:
   - uiautomator2 `swipe_points` from `(material.x_location, material.y_location)` through drag path to production slot.
   - Re-click factory navigation.

Requires `MaterialInfo.x_location` and `y_location` from [material data](data-and-enums.md).

### Stop behavior

Checks `stop_event` between factories.

---

## `add_commercial_material_to_production.py`

| | |
|---|---|
| **Purpose** | Navigate to the correct commercial building and drag materials into production |
| **Server action** | `ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION` |
| **Signature** | `add_commercial_material_to_production(materials, device_id, stop_event, no_of_materials=11)` |

### Algorithm

1. For each material in the list:
   - Dismiss "missing items" popup if visible.
   - `goto_commercial_building(device_id, material.building_name)` — OCR building name in header region; click factory nav until keyword matches.
   - Swipe `no_of_materials` times from material coords to production slot `(520, 940)`.
   - Dismiss missing-items popup again.

### Key automation calls

- [`take_screenshot_and_read_text`](../simcity/bot/automation/take_screenshot_and_read_text.py) — OCR building name
- [`find_miscellaneous_material`](../simcity/bot/automation/find_material.py) (`MISSING_ITEMS`)
- [`perform_swipe`](../simcity/bot/automation/adb_actions.py)

Building keywords mapped in `fetch_keyword_array()` from [`Building`](../simcity/bot/enums/building.py) enum values.

### Stop behavior

Checks `stop_event` between materials and between swipes.

---

## `collect_sold_item_money.py`

| | |
|---|---|
| **Purpose** | Collect coins from sold trade depot listings (recursive, up to 4 page iterations) |
| **Server action** | **None** (standalone only) |
| **Signature** | `collect_sold_item_money(iteration, device_id, stop_event)` |

### Algorithm

1. Ensure trade depot is open (`check_if_trade_depot_open` → `find_and_open_trade_depot` if not).
2. Find `CITY_STORAGE_PURCHASE_COMPLETED` icons; click each.
3. If none found, swipe to next page and recurse with `iteration + 1`.
4. Stop when `iteration == 4`.

### Known issue

Imports `check_if_trade_depot_open` from [`trade_depot.py`](../simcity/bot/automation/trade_depot.py), but that function is **not defined** in the current file. This action will raise `ImportError` if invoked.

### Stop behavior

Checks `stop_event` before work and inside the click loop.

---

## `advertise_all_items_on_trade_depot.py`

| | |
|---|---|
| **Purpose** | Find trade depot coin icons, click advertise, wait 60s per item (5 page iterations) |
| **Server action** | **None** (`ADVERTISE_ITEM_ON_TRADE_DEPOT` prints only in server) |
| **Signature** | `advertise_all_items_on_trade_depot(iteration, device_id, stop_event)` |

### Algorithm

1. Ensure trade depot is open (same as collect — **same import issue**).
2. Find `TRADE_DEPOT_COIN` icons; for each:
   - Click coin → find `ADVERTISE_ICON` → click advertise → wait 60s (checking stop each second).
3. Swipe to next page; recurse until `iteration == 5`.

### Stop behavior

Checks `stop_event` throughout; 60s wait loop is interruptible.

---

## Summary table

| Module | Server action | Checks stop_event |
|--------|---------------|-------------------|
| `buy_items` | `CONTINUOUS_BUY` | No |
| `sell_materials` | `SELL_WITH_FULL_VALUE`, `SELL_WITH_ZERO_VALUE` | Yes |
| `collect_raw_materials` | `COLLECT_FROM_FACTORY` | Yes |
| `add_raw_material_to_production` | `ADD_RAW_MATERIAL_TO_PRODUCTION` | Yes |
| `add_commercial_material_to_production` | `ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION` | Yes |
| `collect_sold_item_money` | — | Yes |
| `advertise_all_items_on_trade_depot` | — (stub in server) | Yes |

## Related documents

- [API](api.md) — how actions are triggered
- [Automation](automation.md) — primitives used by city actions
- [Data and enums](data-and-enums.md) — `MaterialInfo` fields used in production/sell flows
- [Trade bot](trade-bot.md) — alternative buy implementation reusing `buy_items` helpers
