from __future__ import annotations

from typing import Literal, Optional

import narwhals as nw
from narwhals.typing import Frame, IntoFrame

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class NotPatternMatch(BaseValidationParameters):
    """Expect the column entries to be strings that do not pattern match.

    Parameters:
        column (str): The column name.
        pattern (str): The pattern expression the column should not match.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    """

    def __init__(
        self,
        column: str,
        pattern: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: Optional[float] = 0.00,
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

    def __call__(self, frame: Frame) -> IntoFrame:
        """Expect the column entries to be strings that do not pattern match."""
        return (
            frame.filter(
                nw.col(self.column).cast(nw.String).str.contains(self.pattern) == True,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
