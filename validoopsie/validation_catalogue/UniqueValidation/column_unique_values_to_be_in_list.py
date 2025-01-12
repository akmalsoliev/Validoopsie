from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class ColumnUniqueValuesToBeInList(BaseValidationParameters):
    """Check if the unique values are in the list.

    Args:
        column (str): Column to validate.
        values (list[Union[str, float, int]]): List of values to check.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        values: list[str | int | float],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.values = values

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The column '{self.column}' has unique values that are not in the list."

    def __call__(self, frame: FrameT) -> FrameT:
        """Check if the unique values are in the list."""
        return (
            frame.group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
            .filter(
                nw.col(self.column).is_in(self.values) == False,
            )
        )
