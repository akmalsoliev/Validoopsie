from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class ColumnsSumToBeEqualTo(BaseValidationParameters):
    """Check if the sum of the columns is equal to a specific value.

    Args:
        columns_list (list[str]): List of columns to sum.
        sum_value (float): Value that the columns should sum to.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        columns_list: list[str],
        sum_value: float,
        *args,
        **kwargs: object,
    ) -> None:
        self.columns_list = columns_list
        self.sum_value = sum_value
        self.column = "-".join(self.columns_list) + "-combined"
        super().__init__(self.column, *args, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The columns {self.columns_list} do not sum to {self.sum_value}."

    def __call__(self, frame: FrameT) -> FrameT:
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
