from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation
from validoopsie.util import min_max_arg_check, min_max_filter


class LengthToBeBetween(BaseValidation):
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

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> df = pd.DataFrame({
        ...     "strings1": ["12345", "abcde", "1b3d5", "1234", "4321"],
        ...     "strings2": ["A", "13579", "24680", "12345", "abcde"]
        ... })
        >>> frame = nw.from_native(df)

        >>> # Success case - all strings have lengths between 1 and 5
        >>> validator = LengthToBeBetween(
        ...     "strings2",
        ...     min_value=1,
        ...     max_value=5
        ... )
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Failing case - some strings are outside length range
        >>> validator = LengthToBeBetween("strings1", min_value=1, max_value=4)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # With threshold allowing some failures
        >>> validator_with_threshold = LengthToBeBetween(
        ...     column="strings1",
        ...     min_value=1,
        ...     max_value=4,
        ...     threshold=0.6
        ... )
        >>> result = validator_with_threshold.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # With only min_value specified
        >>> min_validator = LengthToBeBetween(
        ...     column="strings1",
        ...     min_value=4
        ... )
        >>> result = min_validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # With only max_value specified
        >>> max_validator = LengthToBeBetween(
        ...     column="strings2",
        ...     max_value=5
        ... )
        >>> result = max_validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        min_value: int | None = None,
        max_value: int | None = None,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        min_max_arg_check(min_value, max_value)

        super().__init__(column, impact, threshold, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has string lengths outside the range"
            f"[{self.min_value}, {self.max_value}]."
        )

    def __call__(self, frame: Frame) -> Frame:
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
