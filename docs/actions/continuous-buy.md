# CONTINUOUS_BUY — Continuous Buy from Global Trade HQ

[← Action guides index](README.md) · [API reference](../api.md)

**Summary:** Repeatedly searches Global Trade HQ (GTHQ) for **all** selected materials in parallel, buys any match immediately, sweeps each visited mayor's depot for other requested items, and paces around the ~30-second GTHQ refresh cycle.

## When to use

- Farm one or more materials from GTHQ overnight or during idle time.
- API-driven multi-material buying (all entries in `selectedMaterials` are active targets).
- Run one buy loop per emulator port; use separate ports for multiple cities.

## API contract

| Field | Required | Usage |
|-------|----------|-------|
| `port` | Yes | Emulator ADB port |
| `action` | Yes | `"CONTINUOUS_BUY"` |
| `selectedMaterials` | Yes | **All** materials are searched on every HQ page (list order = priority tie-breaker on same screen only) |
| `factoriesCount` | No | Ignored |

### Example request

```bash
curl -X POST http://127.0.0.1:5000/action-perform \
  -H "Content-Type: application/json" \
  -d "{\"port\": \"5555\", \"action\": \"CONTINUOUS_BUY\", \"selectedMaterials\": [\"STORAGE_BARS\", \"STORAGE_LOCK\", \"STORAGE_CAMERA\"]}"
```

### Handler

`CONTINUOUS_BUY` dispatches [`run_trade_session`](../../simcity/bot/trade_bot/orchestrator/trade_session.py) with a `PurchaseItem` list built from `selectedMaterials`. Low-level buy clicks still use helpers in [`buy_items.py`](../../simcity/bot/city_actions/buy_items.py).

| Argument | Source |
|----------|--------|
| `purchase_items` | One `PurchaseItem` per `selectedMaterials` entry |
| `device_id` | `port` |
| `stop_event` | Appended by `start_action` |

Empty `selectedMaterials` returns HTTP 400.

## In-game behavior

1. Opens the purchase menu and navigates to Global Trade HQ.
2. Enters a loop (up to 10,000 cycles):
   - Taps Best Value, then reopens GTHQ.
   - **HQ pass** — scans up to 5 pages (configurable via `TradeBotConfig.hq_trade_views`):
     - On each page, **parallel template-matches all requested items**.
     - On any match: visits that mayor's depot, buys the matched item, **sweeps the depot** for other requested items, returns to GTHQ, **resumes the same page pass** (does not restart from page 1 mid-pass).
     - When a page has no more ads to visit, swipes to the next page.
   - After all pages are scanned, waits for the ~30s refresh window.
3. Repeats until stopped or cycle limit.

## Flow diagram

```mermaid
flowchart TD
    start[Build PurchaseItem list] --> session[Outer cycle]
    session --> refresh[Best Value + reopen GTHQ]
    refresh --> pass[HQ pass pages 1..5]
    pass --> detectAll[Parallel-detect ALL items on page]
    detectAll -->|no hits| nextPage[Swipe to next page]
    detectAll -->|hit| visit[Enter mayor depot]
    visit --> buyMatched[Buy matched item]
    buyMatched --> sweep[Sweep depot for other items]
    sweep --> returnHQ[Return to GTHQ]
    returnHQ --> rescan[Rescan same page or continue]
    rescan -->|more ads| visit
    rescan -->|page clear| nextPage
    nextPage --> pass
    pass -->|all pages done| timerWait[Wait GTHQ refresh]
    timerWait --> session
```

## Reading the logs

Logs go to the console and `simcity_buildit.log` (via `setup_logging()` in [`main.py`](../../simcity/bot/main.py)).

Continuous buy lines use the prefix `[CONTINUOUS_BUY][PHASE][city_PORT]`:

| Phase | Meaning |
|-------|---------|
| `API` | Request received, thread started, stop requested |
| `SESSION` | Cycle start/end, shopping list, buy totals |
| `HQ` | Page scan, swipe, pass complete |
| `DETECT` | Template hits, pick decision |
| `DEPOT` | Mayor depot travel, buy, sweep |
| `NAV` | Return to GTHQ, restore page index |
| `TIMER` | Refresh window waits |
| `STOP` | Cooperative stop honored |

Example:

```
[CONTINUOUS_BUY][API][city_5555] CONTINUOUS_BUY received — 3 item(s): STORAGE_BARS, STORAGE_LOCK, STORAGE_CAMERA
[CONTINUOUS_BUY][HQ][city_5555] Page 2/5 — scanning for: STORAGE_BARS, STORAGE_LOCK, STORAGE_CAMERA
[CONTINUOUS_BUY][DETECT][city_5555] Picking "STORAGE_LOCK" at (820, 310) — leftmost/topmost on screen
[CONTINUOUS_BUY][SESSION][city_5555] Cycle buy totals — "STORAGE_BARS": 1, "STORAGE_LOCK": 1, "STORAGE_CAMERA": 0 (grand total: 2)
```

## Automation dependencies

| Type | Used for |
|------|----------|
| ADB clicks | Purchase menu, GTHQ navigation, listing clicks |
| Parallel template matching | All requested items per HQ page (`DetectionService`) |
| uiautomator2 | Horizontal swipe between GTHQ pages |
| Timers | Per-device HQ timer via `global_trade_hq_timer_{port}` |

## Prerequisites & assumptions

- Emulator connected via ADB on the given `port`.
- Game is running and reachable from the city home/trade screens.
- Each `selectedMaterials` entry is a valid `Material` enum name with template data.
- Screen resolution matches swipe coordinates in `TradeBotConfig` (default `1575, 460` → `620, 460`).

## Stop & concurrency

| Mechanism | Effect |
|-----------|--------|
| `POST /action-stop` | Sets `stop_event`; honored between steps and during waits |
| New action on same port | Preempts thread (old stop event set, new thread starts) |
| Loop limit | Exits after 10,000 outer cycles |

## Related code

- API dispatch: [`server.py`](../../simcity/bot/server.py)
- Session: [`trade_session.py`](../../simcity/bot/trade_bot/orchestrator/trade_session.py)
- Buy primitives: [`buy_items.py`](../../simcity/bot/city_actions/buy_items.py)
- Enum: `CityAction.CONTINUOUS_BUY` in [`city_actions.py`](../../simcity/bot/enums/city_actions.py)
- Technical reference: [city-actions — buy_items](../city-actions.md#buy_itemspy)
