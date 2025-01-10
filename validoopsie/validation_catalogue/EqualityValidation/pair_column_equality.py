from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class PairColumnEquality(BaseValidationParameters):
    """Check if the pair of columns are equal.

    Args:
        column (str): Column to validate.
        target_column (str): Column to compare.
        group_by_combined (bool, optional): Group by combine columns. Default True.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        target_column: str,
        *args,
        group_by_combined: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.target_column = target_column
        self.group_by_combined = group_by_combined

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' is not equal to the column"
            f"'{self.target_column}'."
        )

    def __call__(self, frame: FrameT) -> FrameT:
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
