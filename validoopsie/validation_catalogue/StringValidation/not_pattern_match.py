from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class NotPatternMatch(BaseValidation):
    """Expect the column entries to be strings that do not pattern match.

    Parameters:
        column (str): The column name.
        pattern (str): The pattern expression the column should not match.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> df = pd.DataFrame({
        ...     "codes": ["ABC001", "ABC002", "DEF001", "XYZ999", "LMNO12"],
        ...     "codes2": ["BC001", "BC002", "DEF001", "XYZ999", "LMNO12"]
        ... })
        >>> frame = nw.from_native(df)

        >>> # Success case - no values match the pattern
        >>> validator = NotPatternMatch("codes2", pattern="^ABC")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Failing case - some values match the pattern
        >>> validator = NotPatternMatch("codes", pattern="^ABC")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # With threshold allowing some failures
        >>> validator_with_threshold = NotPatternMatch(
        ...     column="codes",
        ...     pattern="^ABC",
        ...     threshold=0.6
        ... )
        >>> result = validator_with_threshold.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        pattern: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)
        self.pattern = pattern

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has entries that do not match "
            f"the pattern '{self.pattern}'."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Expect the column entries to be strings that do not pattern match."""
        return (
            frame.filter(
                nw.col(self.column).cast(nw.String).str.contains(self.pattern) == True,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
