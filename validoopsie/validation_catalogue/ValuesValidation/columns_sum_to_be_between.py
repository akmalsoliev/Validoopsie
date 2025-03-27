from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation
from validoopsie.util import min_max_arg_check, min_max_filter

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnsSumToBeBetween(BaseValidation):
    """Check if the sum of columns is greater than or equal to `max_sum`.

    If the `min_value` or `max_value` is not provided then other will be used as the
    threshold.

    If neither `min_value` nor `max_value` is provided, then the validation will result
    in failure.

    Args:
        columns_list (list[str]): List of columns to sum.
        min_sum_value (float | None): Minimum sum value that columns should be greater
            than or equal to.
        max_sum_value (float | None): Maximum sum value that columns should be less than
            or equal to.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate macronutrient sum in range
        >>> df = pd.DataFrame({
        ...     "protein": [26],
        ...     "fat": [19],
        ...     "carbs": [0]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .ValuesValidation.ColumnsSumToBeBetween(
        ...         columns_list=["protein", "fat", "carbs"],
        ...         min_sum_value=30,
        ...         max_sum_value=50
        ...     )
        ... )
        >>> key = "ColumnsSumToBeBetween_protein-fat-carbs-combined"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        columns_list: list[str],
        min_sum_value: float | None = None,
        max_sum_value: float | None = None,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
    ) -> None:
        min_max_arg_check(min_sum_value, max_sum_value)

        self.columns_list = columns_list
        self.max_sum_value = max_sum_value
        self.min_sum_value = min_sum_value
        self.column = "-".join(self.columns_list) + "-combined"
        super().__init__(self.column, impact, threshold, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The columns {self.columns_list} are not between {self.min_sum_value} and "
            f"{self.max_sum_value}."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Check if the sum of columns is greater than or equal to `max_sum`."""
        # This is just in case if there is some weird column name, such as "sum"
        col_name = "-".join(self.columns_list) + "-sum"
        summed_frame = frame.select(self.columns_list).with_columns(
            nw.sum_horizontal(self.columns_list).alias(col_name),
        )

        return (
            min_max_filter(
                summed_frame,
                col_name,
                self.min_sum_value,
                self.max_sum_value,
            )
            .with_columns(
                nw.concat_str(
                    [nw.col(column) for column in self.columns_list],
                    separator=" - ",
                ).alias(
                    self.column,
                ),
            )
            .group_by(
                self.column,
            )
            .agg(
                nw.col(self.column).count().alias(f"{self.column}-count"),
            )
        )
