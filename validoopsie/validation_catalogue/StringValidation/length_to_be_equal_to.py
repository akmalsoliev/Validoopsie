from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class LengthToBeEqualTo(BaseValidationParameters):
    """Expect the column entries to be strings with length equal to `value`.

    Args:
        column (str): The column name.
        value (int): The expected value for a column entry length.
        threshold (float, optional): The threshold for the validation. Defaults to 0.0.
        impact (str, optional): The impact level of the validation. Defaults to "low".
        kwargs (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        value: int,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.value = value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has entries with length not "
            f"equal to {self.value}."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Expect the column entries to be strings with length equal to `value`.

        Return will be used in the `__execute_check__` method in `column_check`
        decorator.
        """
        return (
            frame.filter(
                nw.col(self.column).str.len_chars() != self.value,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
