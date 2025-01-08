from __future__ import annotations

import narwhals as nw
from narwhals.typing import FrameT

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class NotPatternMatch(BaseValidationParameters):
    """Expect the column entries to be strings that match a given like pattern.

    Args:
        column (str): The column name.
        pattern (str): The pattern expression the column should match.
        threshold (float, optional): The threshold for the validation. Defaults to 0.0.
        impact (str, optional): The impact level of the validation. Defaults to "low".
        kwargs (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str,
        pattern: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(column, *args, **kwargs)
        self.pattern = pattern

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has entries that do not match "
            f"the pattern '{self.pattern}'."
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """Expect the column entries to be strings that match a given like pattern.

        Return will be used in the `__execute_check__` method in `column_check`
        decorator.
        """
        return (
            frame.filter(
                nw.col(self.column).str.contains(self.pattern) == True,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
