from __future__ import annotations

from datetime import date, datetime


def min_max_arg_check(
    min_: float | date | datetime | None,
    max_: float | date | datetime | None,
) -> None:
    """Check if either min or max is provided.

    Parameters:
        min_ (float | None): Minimum
        max_ (float | None): Maximum

    """
    if min_ is None and max_ is None:
        error_msg = "Either min or max must be provided."
        raise ValueError(error_msg)
