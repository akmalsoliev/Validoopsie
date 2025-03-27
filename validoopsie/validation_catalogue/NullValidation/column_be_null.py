from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnBeNull(BaseValidation):
    """Check if the values in a column are null.

    Args:
        column (str): Column to validate.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate field contains only nulls
        >>> df = pd.DataFrame({
        ...     "id": [1, 2, 3],
        ...     "optional_field": [None, None, None]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .NullValidation.ColumnBeNull(column="optional_field")
        ... )
        >>> key = "ColumnBeNull_optional_field"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
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
