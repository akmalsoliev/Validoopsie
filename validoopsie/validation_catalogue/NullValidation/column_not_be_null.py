from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnNotBeNull(BaseValidation):
    """Check if the values in a column are not null.

    Args:
        column (str): Column to validate.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate field has no nulls
        >>> df = pd.DataFrame({
        ...     "id": [1, 2, 3],
        ...     "required_field": ["a", "b", "c"]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .NullValidation.ColumnNotBeNull(column="required_field")
        ... )
        >>> key = "ColumnNotBeNull_required_field"
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
        return f"The column '{self.column}' has values that are null."

    def __call__(self, frame: Frame) -> Frame:
        """Check if the values in a column are not null."""
        null_count_col = f"{self.column}-count"
        return (
            frame.filter(
                nw.col(self.column).is_null() == True,
            )
            .with_columns(nw.lit(1).alias(null_count_col))
            .group_by(self.column)
            .agg(nw.col(null_count_col).sum())
        )
