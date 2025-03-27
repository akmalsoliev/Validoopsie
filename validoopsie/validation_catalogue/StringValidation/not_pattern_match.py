from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class NotPatternMatch(BaseValidation):
    """Expect the column entries to be strings that do not pattern match.

    Args:
        column (str): The column name.
        pattern (str): The pattern expression the column should not match.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of
            validation. Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate text doesn't contain pattern
        >>> df = pd.DataFrame({
        ...     "comment": ["Great product!", "Normal comment", "Just okay"]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .StringValidation.NotPatternMatch(
        ...         column="comment",
        ...         pattern=r"password"
        ...     )
        ... )
        >>> key = "NotPatternMatch_comment"
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
        """Expect the column entries to be strings that do not pattern match."""
        return (
            frame.filter(
                nw.col(self.column).cast(nw.String).str.contains(self.pattern) == True,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
