from __future__ import annotations

import narwhals as nw
from narwhals.typing import Frame, FrameT


def min_max_filter(
    frame: FrameT,
    column: str,
    min_: float | None,
    max_: float | None,
) -> FrameT:
    if min_ and max_:
        return frame.filter(nw.col(column).is_between(min_, max_, closed="both") == False)
    if min_:
        return frame.filter((nw.col(column) >= min_) == False)
    if max_:
        return frame.filter((nw.col(column) <= max_) == False)
    return Frame
