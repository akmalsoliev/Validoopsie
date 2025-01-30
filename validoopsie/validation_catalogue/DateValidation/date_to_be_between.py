from __future__ import annotations

from datetime import date, datetime

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper
from validoopsie.util import min_max_arg_check, min_max_filter


@base_validation_wrapper
class DateToBeBetween(BaseValidationParameters):
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
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        min_date: date | datetime | None = None,
        max_date: date | datetime | None = None,
        *args,
        **kwargs,
    ) -> None:
        min_max_arg_check(min_date, max_date)

        super().__init__(column, *args, **kwargs)
        self.min_date = min_date
        self.max_date = max_date

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has date range outside "
            f"[{self.min_date}, {self.max_date}]."
        )

    def __call__(self, frame: FrameT) -> FrameT | ValueError:
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
