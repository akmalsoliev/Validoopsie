from __future__ import annotations

import re

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class ColumnMatchDateFormat(BaseValidationParameters):
    """Check if the values in a column match the date format.

    Args:
        column (str): Column to validate.
        date_format (str): Date format to check.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        date_format: str,
        *args,
        **kwargs,
    ) -> None:
        self.date_format = date_format
        super().__init__(column, *args, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The column '{self.column}' has unique values that are not in the list."

    def __call__(self, frame: FrameT) -> FrameT:
        """Check if the values in a column match the date format."""
        date_patterns = re.findall(r"[Ymd]+", self.date_format)
        separators = re.findall(r"[^Ymd]+", self.date_format)

        pattern_parts = []
        for i, date_p in enumerate(date_patterns):
            pattern_parts.append(rf"\d{{{len(date_p)}}}")
            if i < len(separators):
                pattern_parts.append(re.escape(separators[i]))

        pattern = "^" + "".join(pattern_parts) + "$"
        exp = nw.col(self.column).str.contains(pattern).alias("contains")
        return (
            frame.with_columns(exp)
            .filter(nw.col("contains") == False)
            .select(nw.col(self.column))
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
