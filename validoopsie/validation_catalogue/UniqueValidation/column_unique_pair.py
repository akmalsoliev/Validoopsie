from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class ColumnUniquePair(BaseValidation):
    """Validates the uniqueness of combined values from multiple columns.

    This class checks if the combination of values from specified columns creates unique
    entries in the dataset. For example, if checking columns ['first_name', 'last_name'],
    the combination of these values should be unique for each row.

    Parameters
      column_list (list | tuple): List or tuple of column names to check for unique
          combinations.
      threshold (float, optional): Threshold for validation. Defaults to 0.0.
      impact (Literal["low", "medium", "high"], optional): Impact level of validation.
          Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> df = pd.DataFrame({
        ...     "first_name": ["John", "Jane", "John", "Alice", "Bob"],
        ...     "last_name": ["Doe", "Smith", "Smith", "Johnson", "Wilson"],
        ...     "age": [30, 25, 35, 28, 42],
        ...     "city": ["NY", "LA", "NY", "Chicago", "Boston"]
        ... })
        >>> frame = nw.from_native(df)

        >>> # Failing case - first_name and city have duplicates
        >>> validator = ColumnUniquePair(["first_name", "city"])
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # Success case - first_name and age combinations are unique
        >>> validator = ColumnUniquePair(["first_name", "age"])
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Success case with multiple columns
        >>> validator = ColumnUniquePair(["first_name", "last_name", "city"])
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column_list: list[str] | tuple[str, ...],
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
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
