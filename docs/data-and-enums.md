# Data and Enums

[← Back to index](README.md)

Material metadata, UI icon references, and domain enums drive template matching and action configuration across the bot.

---

## MaterialInfo

Defined in [`simcity/bot/material_info.py`](../simcity/bot/material_info.py):

```python
@dataclass
class MaterialInfo:
    name: Material
    x_location: int
    y_location: int
    hq_templates: HqTemplates
    depot_templates: DepotTemplates
    base_price: int
    actual_price: int
    storage_template: str
    sell_duration: int
    building_name: str
    manufacturing_recipes: Dict[str, Dict[str, int]] = field(default_factory=dict)
```

| Field | Used by |
|-------|---------|
| `name` | Logging, enum lookup |
| `x_location`, `y_location` | Drag/swipe start point for production actions |
| `hq_templates` | `find_material_in_global_trade_hq`, `trade_bot` detection |
| `depot_templates` | `find_material_in_trade_depot`, depot sweep |
| `storage_template` | `find_material_in_city_storage` during sell |
| `base_price`, `actual_price` | Sell pricing (full vs zero uses `sell_material`) |
| `sell_duration` | Time to hold sell button in sell dialog |
| `building_name` | Commercial production navigation (`Building` enum value or empty for factory items) |
| `manufacturing_recipes` | Recipe metadata (optional) |

### Template dataclasses

- **`HqTemplates`** — `base`, `x1`..`x5` paths for Global Trade HQ quantity variants
- **`DepotTemplates`** — same structure for visiting mayor depots

Paths are relative to the `resources/` image root (resolved by [`take_template.get_image_path`](../simcity/bot/automation/take_template.py)).

---

## Loading pipeline

[`material_data_loader.py`](../simcity/bot/material_data_loader.py):

1. On first call, iterate all `*.json` files in [`resources/material_data/`](../resources/material_data/).
2. For each JSON array entry, construct a `MaterialInfo` keyed by `material.name` (string).
3. Write a cache file [`data.json`](../data.json) at project root with all materials serialized.
4. Return the in-memory `material_info_dict` singleton.

Called by:

- [`server.py`](../simcity/bot/server.py) on every `/action-perform` (resolves `selectedMaterials`)
- [`main.py`](../simcity/bot/main.py) at import (`material_dict`)
- `trade_bot` `DetectionService` for template paths

### JSON entry example

From [`resources/material_data/storage.json`](../resources/material_data/storage.json):

```json
{
  "name": "STORAGE_CAMERA",
  "x_location": 665,
  "y_location": 375,
  "hq_templates": {
    "base": "global_trade_hq/special/storage/camera.png",
    "x1": "global_trade_hq/special/storage/camera_x1.png",
    ...
  },
  "depot_templates": { ... },
  "base_price": 487,
  "actual_price": 10,
  "storage_template": "city_storage/special/storage/camera.png",
  "sell_duration": 5500,
  "building_name": ""
}
```

### JSON files by category

| File | Content |
|------|---------|
| `raw_materials.json` | Factory raw materials |
| `storage.json` | Storage expansion items |
| `beach.json`, `vu.json`, `expansion.json` | Special categories |
| `building_supplies_store.json`, `fashion_store.json`, … | Commercial building products (one file per building type) |

Full list: 24 JSON files under [`resources/material_data/`](../resources/material_data/).

---

## Enums

### Material (`enums/material.py`)

140+ enum members covering raw materials, commercial products, regional items, storage expansions, and special items. Names are **SCREAMING_SNAKE_CASE** strings (e.g. `STORAGE_BARS`, `WOOD`, `PLASTIC`).

- JSON `name` field must match an enum member name.
- Server `selectedMaterials` array uses these string names.
- Do not duplicate the full list here — see the source file.

### Miscellaneous (`enums/miscellaneous.py`)

Maps UI icon identifiers to template image paths under `resources/`. Used by `find_miscellaneous_material`. Examples:

| Member | Typical use |
|--------|-------------|
| `COIN` | HQ view ready detection |
| `TRADE_BOX` | Visiting depot open detection |
| `EMPTY_TRADE_BOXES` | Sell flow — find empty slots |
| `BUY_ICON` | Dismiss buy prompts on depot |
| `CITY_STORAGE_PURCHASE_COMPLETED` | Collect sold item money |
| `TRADE_DEPOT_COIN` | Advertise flow |
| `ADVERTISE_ICON` | Click advertise button |
| `MISSING_ITEMS` | Dismiss missing-items popup |
| `GLOBAL_TRADE_HQ_CHECK`, `GLOBAL_PURCHASE_MENU` | Trade depot open detection |

### Building (`enums/building.py`)

Commercial building types. `get_commercial_building()` returns the list. Values match `building_name` in JSON and keyword arrays in [`add_commercial_material_to_production`](../simcity/bot/city_actions/add_commercial_material_to_production.py).

### CityAction (`enums/city_actions.py`)

Human-readable labels for UI clients:

| Enum member | Value |
|-------------|-------|
| `CONTINUOUS_BUY` | "Continuous Buy" |
| `SELL_WITH_FULL_VALUE` | "Sell with full value" |
| `SELL_WITH_ZERO_VALUE` | "Sell with zero value" |
| `COLLECT_FROM_FACTORY` | "Collect from factory" |
| `COLLECT_FROM_COMMERCIAL` | "Collect from commercial" |
| `COLLECT_SOLD_ITEM_MONEY` | "Collect sold item Money" |
| `ADVERTISE_ITEM_ON_TRADE_DEPOT` | "Advertise item on trade depot" |
| `ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION` | "Add commercial to production" |
| `ADD_RAW_MATERIAL_TO_PRODUCTION` | "Add raw material to production" |

The server uses **enum member names** as `action` strings, not the human-readable values.

### CityNames (`enums/city_names.py`)

Regional city display names for template matching in regional trade flows.

---

## Priority mapping (server)

In [`server.py`](../simcity/bot/server.py), when `selectedMaterials` is non-empty:

```python
for index, material in enumerate(request_data['selectedMaterials']):
    select_material_list.append(material_dict[material])
    material_priorities[Material[material]] = index + 1
```

Lower index = higher priority (1-based). **Currently** this `material_priorities` dict is built but not passed to city action handlers. Multi-material priority buying is handled by `trade_bot` instead.

---

## Resource layout

```
resources/
└── material_data/          # JSON metadata (loaded at runtime)
    ├── raw_materials.json
    ├── storage.json
    ├── fashion_store.json
    └── ...
```

Template images referenced in JSON (e.g. `global_trade_hq/special/storage/camera.png`) are resolved relative to `resources/` by the automation layer.

Screenshots captured at runtime go to `screenshots/city_{device_id}/` (not under `resources/`).

---

## Related documents

- [City actions](city-actions.md) — how `MaterialInfo` fields are used in workflows
- [Automation](automation.md) — template matching pipeline
- [API](api.md) — `selectedMaterials` in requests
- [Trade bot](trade-bot.md) — `PurchaseItem` and config-based material lists
