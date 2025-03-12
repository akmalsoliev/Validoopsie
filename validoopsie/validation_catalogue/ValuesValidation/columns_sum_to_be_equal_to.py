from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class ColumnsSumToBeEqualTo(BaseValidation):
    """Check if the sum of the columns is equal to a specific value.

    Parameters:
        columns_list (list[str]): List of columns to sum.
        sum_value (float): Value that the columns should sum to.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> df = pd.DataFrame({
        ...     "A": [1, 2, 3, 4, 5],
        ...     "B": [5, 4, 3, 2, 1],
        ...     "D": [5, 4, 3, 2, 2]
        ... })
        >>> frame = nw.from_native(df)

        >>> # Success case - A + B sums to 6 in all rows
        >>> validator = ColumnsSumToBeEqualTo(["A", "B"], sum_value=6)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Failing case - A + D does not sum to 6 in all rows
        >>> validator = ColumnsSumToBeEqualTo(["A", "D"], sum_value=6)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # Success case with threshold
        >>> validator = ColumnsSumToBeEqualTo(
        ...     columns_list=["A", "D"],
        ...     sum_value=6,
        ...     threshold=0.5
        ... )
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        columns_list: list[str],
        sum_value: float,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        self.columns_list = columns_list
        self.sum_value = sum_value
        self.column = "-".join(self.columns_list) + "-combined"
        super().__init__(self.column, impact, threshold, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The columns {self.columns_list} do not sum to {self.sum_value}."

    def __call__(self, frame: Frame) -> Frame:
        """Check if the sum of the columns is equal to a specific value."""
        # This is just in case if there is some weird column name, such as "sum"
        col_name = "-".join(self.columns_list) + "-sum"
        return (
            frame.select(self.columns_list)
            .with_columns(
                nw.sum_horizontal(self.columns_list).alias(col_name),
            )
            .filter(
                nw.col(col_name) != self.sum_value,
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
