from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Optional, Sequence, Tuple

import cv2
import numpy as np

from simcity.bot.automation.find_material import perform_matching
from simcity.bot.automation.take_template import take_template
from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.trade_bot.config.defaults import TradeBotConfig
from simcity.bot.trade_bot.models.purchase_item import PurchaseItem
from simcity.bot.trade_bot.utils.image_storage import (
    build_capture_name,
    save_scanned_image,
)

logger = logging.getLogger("trade_bot")

Candidate = Tuple[PurchaseItem, List[int]]


def _where_plain(phase: str) -> str:
    if phase == "hq":
        return "this trade depot view"
    if phase == "depot":
        return "this mayor’s depot"
    return "the screen"


def _to_gray_2d(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    if image.ndim == 3 and image.shape[2] >= 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def _template_fits_screenshot(
    screenshot: np.ndarray,
    template: np.ndarray,
    *,
    item_name: str,
    template_path: str,
) -> bool:
    """``cv2.matchTemplate`` requires template width/height <= image."""
    sh, sw = screenshot.shape[:2]
    th, tw = template.shape[:2]
    if th > sh or tw > sw:
        logger.warning(
            'Can’t look for "%s" — the reference picture is bigger than the game screenshot '
            "(%dx%d vs %dx%d). Use a smaller icon crop or match your screen resolution.",
            item_name,
            tw,
            th,
            sw,
            sh,
        )
        return False
    return True


def _iou(a: List[int], b: List[int]) -> float:
    ax1, ay1, ax2, ay2 = int(a[0]), int(a[1]), int(a[2]), int(a[3])
    bx1, by1, bx2, by2 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    inter = (ix2 - ix1) * (iy2 - iy1)
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    union = area_a + area_b - inter
    return float(inter / union) if union > 0 else 0.0


class DetectionService:
    def __init__(self, config: TradeBotConfig) -> None:
        self._config = config

    def detect_parallel_hq(
        self,
        items: Sequence[PurchaseItem],
        screenshot: np.ndarray,
        stop_check: Optional[Callable[[], bool]] = None,
        view_index: int = 0,
    ) -> List[Candidate]:
        return self._detect_parallel_template_paths(
            items,
            screenshot,
            lambda it: it.resolved_hq_template_path(),
            stop_check,
            phase="hq",
            scan_index=view_index,
            stop_after_best_priority=True,
        )

    def detect_parallel_depot(
        self,
        items: Sequence[PurchaseItem],
        screenshot: np.ndarray,
        stop_check: Optional[Callable[[], bool]] = None,
        page_index: int = 0,
    ) -> List[Candidate]:
        mat_data = load_material_info_data()

        def depot_path(it: PurchaseItem) -> str:
            return mat_data[it.material.name].depot_templates.base

        return self._detect_parallel_template_paths(
            items,
            screenshot,
            depot_path,
            stop_check,
            phase="depot",
            scan_index=page_index,
            stop_after_best_priority=False,
        )

    def _detect_parallel_template_paths(
        self,
        items: Sequence[PurchaseItem],
        screenshot: np.ndarray,
        template_path_fn: Callable[[PurchaseItem], str],
        stop_check: Optional[Callable[[], bool]],
        *,
        phase: str,
        scan_index: int,
        stop_after_best_priority: bool,
    ) -> List[Candidate]:
        items_list = list(items)
        if not items_list:
            return []

        names = ", ".join(it.name for it in items_list)
        where = _where_plain(phase)
        idx_noun = "view" if phase == "hq" else "page"
        logger.info(
            "Searching %s for: %s (%s %s).",
            where,
            names,
            idx_noun,
            scan_index + 1,
        )

        if self._config.save_scans:
            stem = build_capture_name(
                self._config.capture_session_id,
                phase,
                scan_index,
                None,
                "raw",
            )
            save_scanned_image(
                screenshot,
                config=self._config,
                relative_dir=f"{phase}/raw",
                filename_stem=stem,
            )

        candidates: List[Candidate] = []
        best_priority_value = min((it.priority for it in items_list), default=0)

        def work(item: PurchaseItem) -> Optional[Candidate]:
            if stop_check and stop_check():
                return None
            path = template_path_fn(item)
            template = take_template(path)
            if template is None:
                logger.warning(
                    'Can’t look for "%s" — the picture file is missing or unreadable (%s).',
                    item.name,
                    path,
                )
                return None
            scr = _to_gray_2d(screenshot)
            tpl = _to_gray_2d(template)
            if scr.size == 0 or tpl.size == 0:
                logger.warning(
                    'Something went wrong with the image for "%s" — skipping this check.',
                    item.name,
                )
                return None
            if not _template_fits_screenshot(
                scr, tpl, item_name=item.name, template_path=path
            ):
                return None
            rects, _ = perform_matching(
                item.name,
                scr.copy(),
                tpl,
                self._config.match_threshold,
            )
            if not rects:
                return None
            return (item, [int(x) for x in rects[0]])

        with ThreadPoolExecutor(max_workers=max(1, len(items_list))) as ex:
            futures = [ex.submit(work, it) for it in items_list]
            stop_early = False
            for fut in as_completed(futures):
                if stop_check and stop_check():
                    break
                try:
                    result = fut.result()
                except Exception:
                    logger.exception(
                        "Hit a technical error while looking for an item on screen — continuing with the rest."
                    )
                    continue
                if result:
                    candidates.append(result)
                    if (
                        stop_after_best_priority
                        and result[0].priority == best_priority_value
                    ):
                        logger.info(
                            'Found your top-priority want first ("%s") — no need to scan the rest of this %s.',
                            result[0].name,
                            idx_noun,
                        )
                        stop_early = True
                        break
            if stop_early:
                for f in futures:
                    if not f.done():
                        f.cancel()

        hit_names = [c[0].name for c in candidates]
        where = _where_plain(phase)
        if hit_names:
            logger.info(
                "On %s (%s %s): found %s — %s.",
                where,
                idx_noun,
                scan_index + 1,
                len(hit_names),
                ", ".join(hit_names),
            )
        else:
            logger.info(
                "On %s (%s %s): none of your items appeared.",
                where,
                idx_noun,
                scan_index + 1,
            )

        if self._config.save_scans and candidates:
            flat = self.flatten_sorted_by_priority(candidates)
            deduped = self.dedupe_cross_items(
                flat, self._config.dedup_iou_threshold
            )
            vis = _draw_candidates_bgr(screenshot, deduped)
            stem = build_capture_name(
                self._config.capture_session_id,
                phase,
                scan_index,
                None,
                "annotated",
            )
            save_scanned_image(
                vis,
                config=self._config,
                relative_dir=f"{phase}/annotated",
                filename_stem=stem,
            )

        return candidates

    def flatten_sorted_by_priority(
        self,
        candidates: Sequence[Candidate],
    ) -> List[Candidate]:
        return sorted(candidates, key=lambda t: (t[0].priority, t[0].name))

    def dedupe_cross_items(
        self,
        sorted_candidates: Sequence[Candidate],
        iou_threshold: float,
    ) -> List[Candidate]:
        kept: List[Candidate] = []
        for item, rect in sorted_candidates:
            if any(
                _iou(rect, kr) >= iou_threshold
                for _, kr in kept
            ):
                continue
            kept.append((item, rect))
        return kept

    def pick_highest_priority_hit(
        self,
        deduped: Sequence[Candidate],
    ) -> Optional[Candidate]:
        return deduped[0] if deduped else None


def _draw_candidates_bgr(
    screenshot: np.ndarray,
    candidates: Sequence[Candidate],
) -> np.ndarray:
    if screenshot.ndim == 2:
        vis = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)
    else:
        vis = screenshot.copy()
    for _, rect in candidates:
        cv2.rectangle(
            vis,
            (int(rect[0]), int(rect[1])),
            (int(rect[2]), int(rect[3])),
            (0, 255, 0),
            2,
        )
    return vis
