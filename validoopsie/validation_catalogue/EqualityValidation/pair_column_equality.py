from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class PairColumnEquality(BaseValidation):
    """Check if the pair of columns are equal.

    Parameters:
        column (str): Column to validate.
        target_column (str): Column to compare.
        group_by_combined (bool, optional): Group by combine columns. Default True.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> df = pd.DataFrame({
        ...     "column_a": [1, 2, 3, 4, 5],
        ...     "column_b": [1, 2, 3, 4, 5],
        ...     "column_c": [1, 2, 6, 4, 5]
        ... })
        >>> frame = nw.from_native(df)
        >>> validator = PairColumnEquality("column_a", target_column="column_b")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Failing case - some values don't match
        >>> validator = PairColumnEquality("column_a", target_column="column_c")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # With threshold allowing some failures
        >>> validator_with_threshold = PairColumnEquality(
        ...     column="column_a",
        ...     target_column="column_c",
        ...     threshold=0.4
        ... )
        >>> result = validator_with_threshold.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        target_column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        *,
        group_by_combined: bool = True,
        **kwargs: dict[str, object],
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)
        self.target_column = target_column
        self.group_by_combined = group_by_combined

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' is not equal to the column"
            f"'{self.target_column}'."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Check if the pair of columns are equal."""
        select_columns = [self.column, f"{self.column}-count"]
        gb_cols = (
            [self.column, self.target_column] if self.group_by_combined else [self.column]
        )

        validated_frame = (
            frame.filter(
                nw.col(self.column) != nw.col(self.target_column),
            )
            .group_by(gb_cols)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )

        if self.group_by_combined:
            validated_frame = validated_frame.with_columns(
                nw.concat_str(
                    [
                        nw.col(self.column),
                        nw.col(self.target_column),
                    ],
                    separator=f" - column {self.column} - column {self.target_column} - ",
                ).alias(self.column),
            )

        return validated_frame.select(select_columns)
