from __future__ import annotations

from datetime import date, datetime

import narwhals as nw
from narwhals.typing import FrameT


def min_max_filter(
    frame: FrameT,
    column: str,
    min_: float | date | datetime | None,
    max_: float | date | datetime | None,
) -> FrameT:
    if min_ is not None and max_ is not None:
        return frame.filter(nw.col(column).is_between(min_, max_, closed="both") == False)
    if min_ is not None:
        return frame.filter((nw.col(column) >= min_) == False)
    if max_ is not None:
        return frame.filter((nw.col(column) <= max_) == False)
    return frame
