# Automation Layer

[← Back to index](README.md)

The [`simcity/bot/automation/`](../simcity/bot/automation/) package contains **low-level primitives** for controlling the Android emulator: ADB shell commands, screenshots, OpenCV template matching, Tesseract OCR, and preset UI navigation clicks. City actions and `trade_bot` compose these modules into game workflows.

---

## Vision pipeline

Most visual detection follows this pipeline:

```
ADB screencap → grayscale image → load template → cv2.matchTemplate → NMS → click rectangle
```

| Step | Module | Key function |
|------|--------|--------------|
| Screenshot | [`take_screenshot.py`](../simcity/bot/automation/take_screenshot.py) | `take_bw_screenshot`, `take_color_screenshot` |
| Template load | [`take_template.py`](../simcity/bot/automation/take_template.py) | `take_template(path)`, `get_image_path` |
| Matching | [`find_material.py`](../simcity/bot/automation/find_material.py) | `perform_matching`, `perform_template_matching` |
| NMS | [`apply_nsm.py`](../simcity/bot/automation/apply_nsm.py) | `apply_nms`, `apply_nms_and_draw_rectangle` |
| Click | [`adb_actions.py`](../simcity/bot/automation/adb_actions.py) | `perform_click_with_rectangle` |

Screenshots are stored per device under `screenshots/city_{device_id}/`.

Default match threshold is **0.9** unless overridden per call.

---

## 1. Device I/O

| File | Purpose | Key functions |
|------|---------|---------------|
| [`adb_actions.py`](../simcity/bot/automation/adb_actions.py) | Raw ADB input | `perform_click`, `perform_click_with_rectangle`, `perform_swipe`, `press_esc_key`, `adb_long_press_drag` |
| [`check_adb_devices_and_connect_if_not_connected.py`](../simcity/bot/automation/check_adb_devices_and_connect_if_not_connected.py) | ADB connectivity | `check_adb_devices_and_connect_if_not_connected(device_id)` — runs `adb devices`, `adb connect 127.0.0.1:{port}` if missing |
| [`game_movement_actions.py`](../simcity/bot/automation/game_movement_actions.py) | Preset map swipes | `swipe_top_right`, `swipe_left`, `swipe_right`, `swipe_up`, `swipe_down` |

Called from [`main.set_up()`](../simcity/bot/main.py) on every API request.

---

## 2. Core matchers (`find_material.py`)

Central module for template-based detection. All high-level finders delegate here.

| Function | Searches for | Template source |
|----------|--------------|-----------------|
| `find_miscellaneous_material(misc, device_id)` | UI icons (coins, trade boxes, empty slots, etc.) | [`Miscellaneous`](../simcity/bot/enums/miscellaneous.py) enum → image path |
| `find_material_in_city_storage(material, device_id)` | Material in city/material storage | `material.storage_template` |
| `find_material_in_global_trade_hq(material, device_id)` | Material listing on Global Trade HQ | `material.hq_templates` (base + x1–x5 variants) |
| `find_material_in_trade_depot(material, device_id)` | Material in visiting mayor's depot | `material.depot_templates` |

Lower-level:

- `take_screenshot_and_perform_template_matching` — screenshot + single template
- `perform_template_matching` — match one template against an existing screenshot
- `perform_matching` — core OpenCV match + NMS

### When to use which finder

| Scenario | Use |
|----------|-----|
| UI chrome (coins, buttons, empty boxes) | `find_miscellaneous_material` |
| Own city storage during sell | `find_material_in_city_storage` |
| Global Trade HQ carousel (legacy buy) | `find_material_in_global_trade_hq` |
| Visiting another mayor's depot | `find_material_in_trade_depot` |
| Multi-material HQ scan with priorities | [`find_materials_with_priorities.py`](../simcity/bot/automation/find_materials_with_priorities.py) or `trade_bot` `DetectionService` |
| Batch storage search | [`find_materials_in_city_storage.py`](../simcity/bot/automation/find_materials_in_city_storage.py) |
| Poll until icon appears | [`find_material_count.py`](../simcity/bot/automation/find_material_count.py) |

---

## 3. OCR

| File | Purpose |
|------|---------|
| [`take_screenshot_and_read_text.py`](../simcity/bot/automation/take_screenshot_and_read_text.py) | Crop region from screenshot, Tesseract OCR (digits whitelist option) |
| [`read_text_from_screenshot.py`](../simcity/bot/automation/read_text_from_screenshot.py) | Enhanced OCR with resize, contrast, threshold preprocessing |

Tesseract binary path is set in [`main.py`](../simcity/bot/main.py):

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Used for commercial building name detection and material quantity reading during sell.

---

## 4. UI navigation (`city_utility_actions.py`)

Preset coordinate clicks for game menus and navigation. Examples:

| Function | Action |
|----------|--------|
| `click_on_purchase_menu` | Open purchase / trade menu |
| `click_on_global_trade_hq` | Open Global Trade HQ |
| `click_on_best_value_menu` | Refresh HQ listings |
| `click_on_own_trade_depot` | Open own trade depot |
| `click_on_city_storage` / `click_on_own_material_storage` | Open storage views |
| `click_on_regions_button`, `click_on_limestone_cliff`, etc. | Regional navigation |
| `go_to_next_page_in_city_trade_depot` / `go_to_next_page_in_storage` | Pagination swipes |
| `click_on_home_button`, `click_on_back_button` | Recovery navigation |
| `check_if_i_reach_home` | Home screen detection |

These use **fixed coordinates** tuned for a specific emulator resolution.

---

## 5. Trade depot workflow

| File | Role in flow |
|------|--------------|
| [`go_to_trade_depot_and_open_it.py`](../simcity/bot/automation/go_to_trade_depot_and_open_it.py) | Swipe on city map to reach trade depot |
| [`trade_depot.py`](../simcity/bot/automation/trade_depot.py) | `find_and_open_trade_depot` — detect purchase menu / HQ state, open depot |
| [`open_empty_trade_box.py`](../simcity/bot/automation/open_empty_trade_box.py) | Click an empty trade slot |
| [`sell_material.py`](../simcity/bot/automation/sell_material.py) | Set price/quantity in sell dialog, confirm |
| [`find_empty_trade_boxes_and_sell_material.py`](../simcity/bot/automation/find_empty_trade_boxes_and_sell_material.py) | Standalone sell orchestrator + `capture_material_quantity` (OCR) |
| [`close_trade_depot.py`](../simcity/bot/automation/close_trade_depot.py) | Press ESC to close depot |

Typical sell flow: open depot → find empty boxes → open box → find material in storage → sell → repeat.

---

## 6. Legacy Global Trade HQ buy flow

Older, more complex buy state machine used before `buy_items` and `trade_bot`. Partially superseded but still present in the codebase.

| File | Role |
|------|------|
| [`find_materials_on_global_trade_hq.py`](../simcity/bot/automation/find_materials_on_global_trade_hq.py) | Large state machine: coin detection → multi-material search → visit depot → buy → timer-based refresh |
| [`find_materials_with_priorities.py`](../simcity/bot/automation/find_materials_with_priorities.py) | Parallel multi-material HQ/depot search with priority sort |
| [`click_on_daniel_face_and_goto_daniel_city.py`](../simcity/bot/automation/click_on_daniel_face_and_goto_daniel_city.py) | Navigate to Daniel's city |
| [`find_trade_icon_in_daniel_city.py`](../simcity/bot/automation/find_trade_icon_in_daniel_city.py) | Wait for Daniel trade icon |
| [`find_city_name_and_click_on_trade_hq.py`](../simcity/bot/automation/find_city_name_and_click_on_trade_hq.py) | OCR city name → click regional HQ |
| [`find_and_click_on_refresh_button.py`](../simcity/bot/automation/find_and_click_on_refresh_button.py) | Poll and click refresh |
| [`get_page_one_and_two_waiting_time.py`](../simcity/bot/automation/get_page_one_and_two_waiting_time.py) | Compute wait from timer elapsed |
| [`stop_reset_start_timer.py`](../simcity/bot/automation/stop_reset_start_timer.py) | Timer utility wrapper |
| [`check_for_home_button.py`](../simcity/bot/automation/check_for_home_button.py) / [`check_for_close_button.py`](../simcity/bot/automation/check_for_close_button.py) | Stuck-screen recovery |
| [`check_if_home_button_visible.py`](../simcity/bot/automation/check_if_home_button_visible.py) / [`check_if_close_button_visible.py`](../simcity/bot/automation/check_if_close_button_visible.py) | Visibility checks + click |
| [`check_if_purchase_is_complete.py`](../simcity/bot/automation/check_if_purchase_is_complete.py) | Poll for purchase-complete icon |

**Current production buy paths:** [`buy_items`](../simcity/bot/city_actions/buy_items.py) (API) and [`trade_bot`](../simcity/bot/trade_bot/) (standalone).

---

## 7. Debug utilities

| File | Purpose |
|------|---------|
| [`draw_rectangles_on_screenshot.py`](../simcity/bot/automation/draw_rectangles_on_screenshot.py) | Annotate match rectangles on saved screenshots |
| [`draw_rectangle.py`](../simcity/bot/automation/draw_rectangle.py) | Debug OCR on a fixed screen region |

`trade_bot` can save annotated scan images when `save_scans=True` in config — see [trade-bot.md](trade-bot.md).

---

## Module inventory

All 33 Python modules in `automation/`:

```
adb_actions.py
apply_nsm.py
check_adb_devices_and_connect_if_not_connected.py
check_for_close_button.py
check_for_home_button.py
check_if_close_button_visible.py
check_if_home_button_visible.py
check_if_purchase_is_complete.py
city_utility_actions.py
click_on_daniel_face_and_goto_daniel_city.py
close_trade_depot.py
draw_rectangle.py
draw_rectangles_on_screenshot.py
find_and_click_on_refresh_button.py
find_city_name_and_click_on_trade_hq.py
find_empty_trade_boxes_and_sell_material.py
find_material.py
find_material_count.py
find_materials_in_city_storage.py
find_materials_on_global_trade_hq.py
find_materials_with_priorities.py
find_trade_icon_in_daniel_city.py
game_movement_actions.py
get_page_one_and_two_waiting_time.py
go_to_trade_depot_and_open_it.py
open_empty_trade_box.py
read_text_from_screenshot.py
sell_material.py
stop_reset_start_timer.py
take_screenshot.py
take_screenshot_and_read_text.py
take_template.py
trade_depot.py
```

## Related documents

- [City actions](city-actions.md) — how automation is composed into game tasks
- [Data and enums](data-and-enums.md) — template paths and `Miscellaneous` icons
- [Architecture](architecture.md) — where automation sits in the layer stack
