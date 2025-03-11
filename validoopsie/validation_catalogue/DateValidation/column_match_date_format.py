from __future__ import annotations

import re
from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class ColumnMatchDateFormat(BaseValidation):
    """Check if the values in a column match the date format.

    Parameters:
        column (str): Column to validate.
        date_format (str): Date format to check.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> df = pd.DataFrame(
        ...   {"dates_column": ["2022-01-01", "2022-01-02", "2022-01-03"]}
        ... )
        >>> frame = nw.from_native(df)
        >>> validator = ColumnMatchDateFormat("dates_column", date_format="YYYY-mm-dd")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        # With a failing case
        >>> df_with_error = pd.DataFrame(
        ...     {"dates_column": ["2022-01-01", "2022-01-02", "2024/12/12"]}
        ... )
        >>> frame_with_error = nw.from_native(df_with_error)
        >>> validator = ColumnMatchDateFormat("dates_column", date_format="YYYY-mm-dd")
        >>> result = validator.__execute_check__(frame=frame_with_error)
        >>> result["result"]["status"]
        'Fail'

        # With threshold allowing some failures
        >>> validator_with_threshold = ColumnMatchDateFormat(
        ...     column="dates_column",
        ...     date_format="YYYY-mm-dd",
        ...     threshold=0.5
        ... )
        >>> result = validator_with_threshold.__execute_check__(frame=frame_with_error)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        date_format: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        self.date_format = date_format
        super().__init__(column, impact, threshold, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The column '{self.column}' has unique values that are not in the list."

    def __call__(self, frame: Frame) -> Frame:
        """Check if the values in a column match the date format."""
        date_patterns = re.findall(r"[Ymd]+", self.date_format)
        separators = re.findall(r"[^Ymd]+", self.date_format)

        pattern_parts = []
        for i, date_p in enumerate(date_patterns):
            pattern_parts.append(rf"\d{{{len(date_p)}}}")
            if i < len(separators):
                pattern_parts.append(re.escape(separators[i]))

        pattern = "^" + "".join(pattern_parts) + "$"
        exp = nw.col(self.column).cast(nw.String).str.contains(pattern).alias("contains")
        return (
            frame.with_columns(exp)
            .filter(nw.col("contains") == False)
            .select(nw.col(self.column))
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
