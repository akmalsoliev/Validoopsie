from __future__ import annotations

import re
from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnMatchDateFormat(BaseValidation):
    """Check if the values in a column match the date format.

    Args:
        column (str): Column to validate.
        date_format (str): Date format to check.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate dates match format
        >>> df = pd.DataFrame({
        ...     "dates_iso": ["2023-01-01", "2023-02-15", "2023-03-30"],
        ...     "dates_mixed": ["2023-01-01", "02/15/2023", "2023-03-30"]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .DateValidation.ColumnMatchDateFormat(
        ...         column="dates_iso",
        ...         date_format="YYYY-mm-dd"
        ...     )
        ... )
        >>> key = "ColumnMatchDateFormat_dates_iso"
        >>> vd.results[key]["result"]["status"]
        'Success'

        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()
        >>>
        >>> # With threshold allowing some failures
        >>> vd2 = (
        ...     Validate(df)
        ...     .DateValidation.ColumnMatchDateFormat(
        ...         column="dates_mixed",
        ...         date_format="YYYY-mm-dd",
        ...         threshold=0.4  # Allow 40% failure rate
        ...     )
        ... )
        >>> key2 = "ColumnMatchDateFormat_dates_mixed"
        >>> vd2.results[key2]["result"]["status"]
        'Success'

    """

    def __init__(
        self,
        column: str,
        date_format: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
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
