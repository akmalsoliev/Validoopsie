from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class ColumnNotBeNull(BaseValidationParameters):
    """Check if the values in a column are not null.

    Args:
        column (str): Column to validate.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The column '{self.column}' has values that are null."

    def __call__(self, frame: FrameT) -> FrameT:
        """Check if the values in a column are not null."""
        null_count_col = f"{self.column}-count"
        return (
            frame.filter(
                nw.col(self.column).is_null() == True,
            )
            .with_columns(nw.lit(1).alias(null_count_col))
            .group_by(self.column)
            .agg(nw.col(null_count_col).sum())
        )
