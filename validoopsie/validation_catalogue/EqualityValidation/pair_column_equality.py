from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class PairColumnEquality(BaseValidation):
    """Check if the pair of columns are equal.

    Args:
        column (str): Column to validate.
        target_column (str): Column to compare.
        group_by_combined (bool, optional): Group by combine columns. Default True.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate columns match
        >>> df = pd.DataFrame({
        ...     "amount": [100, 200, 300],
        ...     "verified_amount": [100, 200, 300]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .EqualityValidation.PairColumnEquality(
        ...         column="amount",
        ...         target_column="verified_amount"
        ...     )
        ... )
        >>> key = "PairColumnEquality_amount"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str,
        target_column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        *,
        group_by_combined: bool = True,
        **kwargs: KwargsParams,
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
