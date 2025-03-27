from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnUniqueValuesToBeInList(BaseValidation):
    """Check if the unique values are in the list.

    Args:
        column (str): Column to validate.
        values (list[Union[str, float, int, None]]): List of values to check.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of
            validation. Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate values in allowed list
        >>> df = pd.DataFrame({
        ...     "status": ["active", "inactive", "pending"]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .UniqueValidation.ColumnUniqueValuesToBeInList(
        ...         column="status",
        ...         values=["active", "inactive", "pending"]
        ...     )
        ... )
        >>> key = "ColumnUniqueValuesToBeInList_status"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str,
        values: list[str | int | float | None],
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)
        self.values = values

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The column '{self.column}' has unique values that are not in the list."

    def __call__(self, frame: Frame) -> Frame:
        """Check if the unique values are in the list."""
        return (
            frame.group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
            .filter(
                nw.col(self.column).is_in(self.values) == False,
            )
        )
