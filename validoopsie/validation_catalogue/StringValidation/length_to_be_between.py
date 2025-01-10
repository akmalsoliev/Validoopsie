from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class LengthToBeBetween(BaseValidationParameters):
    """Check if the string lengths are between the specified range.

    Args:
        column (str): Column to validate.
        min_value (float): Minimum value for a column entry length.
        max_value (float): Maximum value for a column entry length.
        closed (str, optional): Closed interval. Defaults to "both".
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

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
        """Check if the string lengths are between the specified range."""
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
