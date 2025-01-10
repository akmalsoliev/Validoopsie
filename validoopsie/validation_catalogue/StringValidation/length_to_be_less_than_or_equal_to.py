from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class LengthToBeLessThanOrEqualTo(BaseValidationParameters):
    """Column string length to be less than or equal to `max_value` characters.

    Args:
        column (str): The column name.
        max_value (float): The maximum value for a column entry length.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        max_value: float,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.max_value = max_value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has string lengths greater than "
            f"{self.max_value}."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Column string length to be less than or equal to `max_value` characters."""
        return (
            frame.filter(
                nw.col(self.column).str.len_chars() > self.max_value,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
