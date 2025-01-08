from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class LengthToBeGreaterThanOrEqualTo(BaseValidationParameters):
    """Column string length to be greater than or equal to `min_value` chars.

    Args:
        column (str): The column name.
        min_value (float): The minimum value for a column entry length.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (str, optional): Impact level of validation. Defaults to "low".
        kwargs:KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        min_value: float,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.min_value = min_value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has string lengths less than {self.min_value}."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Check if the string lengths are greater than or equal to the specified value.

        Return will be used in the `__execute_check__` method in `column_check`
        decorator.
        """
        return (
            frame.filter(
                nw.col(self.column).str.len_chars() < self.min_value,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
