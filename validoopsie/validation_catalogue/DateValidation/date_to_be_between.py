from __future__ import annotations

from datetime import date, datetime
from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation
from validoopsie.util import min_max_arg_check, min_max_filter


class DateToBeBetween(BaseValidation):
    """Check if the column date is between min-max range.

    If the `min_date` or `max_date` is not provided then other will be used as the
    threshold.

    If neither `min_date` nor `max_date` is provided, then the validation will result
    in failure.

    Parameters:
        column (str): Column to validate.
        min_date (int | None): Minimum date for a column entry length.
        max_date (int | None): Maximum date for a column entry length.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> from datetime import date
        >>> df = pd.DataFrame(
        ...     {"dates_column": [date(2023, 1, 1), date(2023, 2, 15), date(2023, 5, 15)]}
        ... )
        >>> frame = nw.from_native(df)
        >>> validator = DateToBeBetween(
        ...     "dates_column",
        ...     min_date=date(2023, 1, 1),
        ...     max_date=date(2023, 5, 15)
        ... )
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        # With only min_date specified
        >>> min_validator = DateToBeBetween(
        ...     column="dates_column",
        ...     min_date=date(2023, 1, 1)
        ... )
        >>> result = min_validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        # With only max_date specified
        >>> max_validator = DateToBeBetween(
        ...     column="dates_column",
        ...     max_date=date(2023, 5, 15)
        ... )
        >>> result = max_validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        min_date: date | datetime | None = None,
        max_date: date | datetime | None = None,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        min_max_arg_check(min_date, max_date)

        super().__init__(column, impact, threshold, **kwargs)
        self.min_date = min_date
        self.max_date = max_date

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has date range outside "
            f"[{self.min_date}, {self.max_date}]."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Check if the string lengths are between the specified range."""
        return (
            min_max_filter(
                frame,
                f"{self.column}",
                self.min_date,
                self.max_date,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
