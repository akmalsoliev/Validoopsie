from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper
from validoopsie.util import min_max_arg_check, min_max_filter


@base_validation_wrapper
class ColumnUniqueValueCountToBeBetween(BaseValidationParameters):
    """Check the number of unique values in a column to be between min and max.

    If the `min_value` or `max_value` is not provided then other will be used as the
    threshold.

    If neither `min_value` nor `max_value` is provided, then the validation will result
    in failure.

    Args:
        column (str): The column to validate.
        min_value (int or None): The minimum number of unique values allowed.
        max_value (int or None): The maximum number of unique values allowed.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        min_value: int | None = None,
        max_value: int | None = None,
        *args,
        **kwargs,
    ) -> None:
        min_max_arg_check(min_value, max_value)

        super().__init__(column, *args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has a number of unique values that "
            f"is not between {self.min_value} and {self.max_value}."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Validate the number of unique values in the column."""
        unique_value_counts = frame.group_by(self.column).agg(
            nw.col(self.column).count().alias(f"{self.column}-count"),
        )

        return min_max_filter(
            unique_value_counts,
            f"{self.column}-count",
            self.min_value,
            self.max_value,
        )
