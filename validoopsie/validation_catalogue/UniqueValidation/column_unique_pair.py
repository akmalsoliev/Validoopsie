from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class ColumnUniquePair(BaseValidation):
    """Validates the uniqueness of combined values from multiple columns.

    This class checks if the combination of values from specified columns creates unique
    entries in the dataset. For example, if checking columns ['first_name', 'last_name'],
    the combination of these values should be unique for each row.

    Args:
        column_list (list | tuple): List or tuple of column names to check for
            unique combinations.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of
            validation. Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate unique pairs
        >>> df = pd.DataFrame({
        ...     "student_id": [101, 102, 103],
        ...     "course_id": [201, 202, 203],
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .UniqueValidation.ColumnUniquePair(
        ...         column_list=["student_id", "course_id"]
        ...     )
        ... )
        >>> key = "ColumnUniquePair_student_id - course_id"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column_list: list[str] | tuple[str, ...],
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
    ) -> None:
        assert len(column_list) > 0, "At least two columns are required."

        self.column_list = column_list
        column = " - ".join(column_list)
        super().__init__(column, impact, threshold, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return a descriptive message when the validation fails."""
        return (
            f"Duplicate entries found: The combination of columns [{self.column}] "
            "contains non-unique values."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Check if the unique values are in the list."""
        return (
            frame.with_columns(
                nw.concat_str(
                    [nw.col(col) for col in self.column_list],
                    separator=" - ",
                ).alias(self.column),
            )
            .group_by(self.column)
            .agg(nw.len().alias(f"{self.column}-count"))
            .filter(nw.col(f"{self.column}-count") > 1)
        )
