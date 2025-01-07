from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class ColumnValuesToBeBetween(BaseValidationParameters):
    """Check if the values in a column are between a range.

    Args:
        column (str): Column to validate.
        min_value (int): Minimum value.
        max_value (int): Maximum value.
        threshold (float, optional): The threshold for the validation. Defaults to 0.0.
        impact (str, optional): The impact level of the validation. Defaults to "low".
        kwargs (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        min_value: float,
        max_value: float,
        *args,
        **kwargs: object,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has values that are not "
            f"between {self.min_value} and {self.max_value}."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Check if the values in a column are between a range.

        Return will be used in the `__execute_check__` method in `column_check`
        decorator.
        """
        return (
            frame.group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
            .filter(
                nw.col(self.column).is_between(self.min_value, self.max_value) == False,
            )
        )
