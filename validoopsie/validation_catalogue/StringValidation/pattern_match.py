from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class PatternMatch(BaseValidation):
    r"""Expect the column entries to be strings that pattern matches.

    Args:
        column (str): The column name.
        pattern (str): The pattern expression the column should match.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate email format
        >>> df = pd.DataFrame({
        ...     "email": ["user1@example.com", "user2@example.com"]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .StringValidation.PatternMatch(
        ...         column="email",
        ...         pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ...     )
        ... )
        >>> key = "PatternMatch_email"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str,
        pattern: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
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
        """Expect the column entries to be strings that pattern matches."""
        return (
            frame.filter(
                nw.col(self.column).cast(nw.String).str.contains(self.pattern) == False,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
