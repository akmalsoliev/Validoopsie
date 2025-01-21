from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper
from validoopsie.util import min_max_arg_check, min_max_filter


@base_validation_wrapper
class LengthToBeBetween(BaseValidationParameters):
    """Check if the string lengths are between the specified range.

    If the `min_value` or `max_value` is not provided then other will be used as the
    threshold.

    If neither `min_value` nor `max_value` is provided, then the validation will result
    in failure.

    Parameters:
        column (str): Column to validate.
        min_value (int | None): Minimum value for a column entry length.
        max_value (int | None): Maximum value for a column entry length.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        min_value: int | None = None,
        max_value: int | None = None,
        *args,
        **kwargs,
    ) -> None:
        min_max_arg_check(min_value, max_value)

        super().__init__(column, *args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has string lengths outside the range"
            f"[{self.min_value}, {self.max_value}]."
        )

    def __call__(self, frame: FrameT) -> FrameT | ValueError:
        """Check if the string lengths are between the specified range."""
        transformed_frame = frame.with_columns(
            nw.col(self.column).str.len_chars().alias(f"{self.column}-length"),
        )

        return (
            min_max_filter(
                transformed_frame,
                f"{self.column}-length",
                self.min_value,
                self.max_value,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
