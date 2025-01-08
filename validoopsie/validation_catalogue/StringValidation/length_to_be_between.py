from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class LengthToBeBetween(BaseValidationParameters):
    """Column string to be between `min_value` and `max_value` number of characters.

    If either `min_value` or `max_value` is None, the check will only consider the other
    value.

    Args:
        column (str): The column name.
        min_value (float): The minimum value for a column entry length.
        max_value (float): The maximum value for a column entry length.
        threshold (float, optional): The threshold for the validation. Defaults to 0.0.
        impact (str, optional): The impact level of the validation. Defaults to "low".
        kwargs (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        min_value: float | None,
        max_value: float | None,
        closed: str = "both",
        *args,
        **kwargs,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.closed = closed

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has string lengths outside the range"
            f"[{self.min_value}, {self.max_value}]."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Check if the string lengths are between the specified range.

        Return will be used in the `__execute_check__` method in `column_check`
        decorator.
        """
        return (
            frame.filter(
                nw.col(self.column)
                .str.len_chars()
                .is_between(self.min_value, self.max_value, closed=self.closed)
                == False,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
