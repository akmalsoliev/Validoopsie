from __future__ import annotations


def min_max_arg_check(min_value: float | None, max_value: float | None) -> None:
    """Check if either min or max is provided.

    Args:
        min_value (float | None): Minimum value.
        max_value (float | None): Maximum value.

    """
    if min_value is None and max_value is None:
        error_msg = "Either min or max must be provided."
        raise ValueError(error_msg)
