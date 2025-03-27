from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation
from validoopsie.util import min_max_arg_check, min_max_filter

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnValuesToBeBetween(BaseValidation):
    """Check if the values in a column are between a range.

    If the `min_value` or `max_value` is not provided then other will be used as the
    threshold.

    If neither `min_value` nor `max_value` is provided, then the validation will result
    in failure.


    Args:
        column (str): Column to validate.
        min_value (float | None): Minimum value for a column entry length.
        max_value (float | None): Maximum value for a column entry length.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate numeric range
        >>> df = pd.DataFrame({
        ...     "age": [25, 30, 42, 18, 65]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .ValuesValidation.ColumnValuesToBeBetween(
        ...         column="age",
        ...         min_value=18,
        ...         max_value=65
        ...     )
        ... )
        >>> key = "ColumnValuesToBeBetween_age"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str,
        min_value: float | None = None,
        max_value: float | None = None,
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
            f"The column '{self.column}' has values that are not "
            f"between {self.min_value} and {self.max_value}."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Check if the values in a column are between a range."""
        return (
            min_max_filter(
                frame,
                f"{self.column}",
                self.min_value,
                self.max_value,
            )
            .group_by(self.column)
            .agg(
                nw.col(self.column).count().alias(f"{self.column}-count"),
            )
        )
