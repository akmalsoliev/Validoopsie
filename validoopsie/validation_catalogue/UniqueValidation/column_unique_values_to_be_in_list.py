from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class ColumnUniqueValuesToBeInList(BaseValidation):
    """Check if the unique values are in the list.

    Parameters:
        column (str): Column to validate.
        values (list[Union[str, float, int, None]]): List of values to check.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> berlin = ["Berlin"] * 4
        >>> rome = ["Rome"] * 5
        >>> df = pd.DataFrame({
        ...     "cities": berlin + rome + ["Paris"]
        ... })
        >>> frame = nw.from_native(df)

        >>> # Failing case - Paris is not in the allowed list
        >>> validator = ColumnUniqueValuesToBeInList("cities", ["Berlin", "Rome"])
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # Success case with threshold
        >>> validator = ColumnUniqueValuesToBeInList(
        ...     column="cities",
        ...     values=["Berlin", "Rome"],
        ...     threshold=0.5
        ... )
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Success case - all values in the allowed list
        >>> validator = ColumnUniqueValuesToBeInList(
        ...     column="cities",
        ...     values=["Paris", "Rome", "Berlin"]
        ... )
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        values: list[str | int | float | None],
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
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
