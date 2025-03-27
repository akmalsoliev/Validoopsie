from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation
from validoopsie.util import min_max_arg_check, min_max_filter

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnUniqueValueCountToBeBetween(BaseValidation):
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

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate number of unique values
        >>> df = pd.DataFrame({
        ...     "category": ["A", "B", "C", "A", "B"]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .UniqueValidation.ColumnUniqueValueCountToBeBetween(
        ...         column="category",
        ...         min_value=1,
        ...         max_value=5
        ...     )
        ... )
        >>> key = "ColumnUniqueValueCountToBeBetween_category"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str,
        min_value: int | None = None,
        max_value: int | None = None,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
    ) -> None:
        min_max_arg_check(min_value, max_value)

        super().__init__(column, impact, threshold, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has a number of unique values that "
            f"is not between {self.min_value} and {self.max_value}."
        )

    def __call__(self, frame: Frame) -> Frame:
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
