from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class ColumnsSumToBeLessEqualTo(BaseValidationParameters):
    """Check if the sum of columns less or equal than `min_sum`.

    Args:
        columns_list (list[str]): List of columns to sum.
        min_sum (float): Min sum value that column should greater or equal to.
        impact (str, optional): The impact level of the validation. Defaults to "low".
        threshold (float, optional): The threshold for the validation. Defaults to 0.0.
        kwargs (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        columns_list: list[str],
        min_sum_value: float,
        *args,
        **kwargs: object,
    ) -> None:
        self.columns_list = columns_list
        self.min_sum_value = min_sum_value
        self.column = "-".join(self.columns_list) + "-combined"
        super().__init__(self.column, *args, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The columns {self.columns_list} are not equal or less than "
            f"{self.min_sum_value}."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Check if the sum of the columns is less or equal to `sum_value`.

        Return will be used in the `__execute_check__` method in `column_check`
        decorator.
        """
        # This is just in case if there is some weird column name, such as "sum"
        col_name = "-".join(self.columns_list) + "-sum"
        return (
            frame.select(self.columns_list)
            .with_columns(
                nw.sum_horizontal(self.columns_list).alias(col_name),
            )
            .filter(
                nw.col(col_name) > self.min_sum_value,
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
