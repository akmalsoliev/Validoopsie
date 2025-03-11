from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidationParameters


class ColumnBeNull(BaseValidationParameters):
    """Check if the values in a column are null.

    Parameters:
        column (str): Column to validate.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    """

    def __init__(
        self,
        column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The column '{self.column}' doesn't have values that are null."

    def __call__(self, frame: Frame) -> Frame:
        """Check if the values in a column are null."""
        return (
            frame.select(self.column)
            .filter(
                nw.col(self.column).is_null() == False,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
