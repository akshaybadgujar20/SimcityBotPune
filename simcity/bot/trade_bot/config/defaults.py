from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from uuid import uuid4


@dataclass
class TradeBotConfig:
    #: Trade depot (Global Trade HQ): how many **views** to check — **3** = 1st as it opens, then swipe right
    #: for 2nd, swipe right again for 3rd. Clamped between 1 and 6.
    hq_trade_views: int = 2
    max_depot_pages: int = 3
    #: Visiting a mayor: if we still need items and see at least this many ``TRADE_BOX`` slot markers on
    #: screen, assume another depot page may exist and swipe. Below this, treat as the last page.
    depot_full_page_trade_box_threshold: int = 8
    #: Visiting a mayor: max time to wait for trade-slot markers after travel (depot-open signal).
    visiting_depot_trade_box_wait_seconds: float = 25.0
    match_threshold: float = 0.9
    nms_threshold: float = 0.6
    dedup_iou_threshold: float = 0.5
    #: Used when swiping inside a mayor’s depot (not between Global Trade HQ views).
    swipe_after_seconds: float = 2.0
    #: Between trade depot views we wait until a coin is seen; poll this often.
    hq_coin_poll_interval_seconds: float = 0.2
    #: Max coin-template checks per trade depot view before treating the screen as empty / not ready.
    #: After this, we use ``hq_empty_pass_wait_seconds`` and the session loop reopens HQ (Best Value, etc.).
    hq_coin_max_poll_attempts: int = 5
    #: After scanning every trade depot view in a pass with no purchase: total seconds from the start of
    #: that pass until we’re ready to open HQ again. We only sleep ``max(0, this - already_spent)``.
    hq_empty_pass_wait_seconds: float = 30.0
    #: After visiting another mayor’s depot: wall-clock period for the game’s trade refresh. We only wait
    #: the **remainder** of this window (from when the 1st HQ view was ready) before searching HQ again.
    hq_trade_refresh_period_seconds: float = 30.0
    hq_swipe_x1: int = 1575
    hq_swipe_y1: int = 460
    hq_swipe_x2: int = 620
    hq_swipe_y2: int = 460
    hq_swipe_duration_s: float = 0.5
    save_scans: bool = False
    capture_session_id: Optional[str] = None
    captures_root_override: Optional[Path] = None

    def __post_init__(self) -> None:
        if self.capture_session_id is None:
            object.__setattr__(self, "capture_session_id", uuid4().hex[:12])
        v = int(self.hq_trade_views)
        if v > 6:
            object.__setattr__(self, "hq_trade_views", 6)
        elif v < 1:
            object.__setattr__(self, "hq_trade_views", 1)
        t = int(self.depot_full_page_trade_box_threshold)
        if t > 16:
            object.__setattr__(self, "depot_full_page_trade_box_threshold", 16)
        elif t < 1:
            object.__setattr__(self, "depot_full_page_trade_box_threshold", 1)
