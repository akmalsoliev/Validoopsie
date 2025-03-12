from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class ColumnBeNull(BaseValidation):
    """Check if the values in a column are null.

    Parameters:
        column (str): Column to validate.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> import numpy as np
        >>> df = pd.DataFrame({
        ...     "col_mixed": [1, 2, None, 4, 5],
        ...     "col_no_nulls": [1.0, 2.0, 3.0, 4.0, 5.0],
        ...     "col_all_nulls": [None, None, None, None, None]
        ... })
        >>> frame = nw.from_native(df)
        >>> validator = ColumnBeNull("col_all_nulls")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Failing case - some values are not null
        >>> validator = ColumnBeNull("col_mixed")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # Failing case - all values are not null
        >>> validator = ColumnBeNull("col_no_nulls")
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # With threshold allowing some non-null values
        >>> validator_with_threshold = ColumnBeNull(
        ...     column="col_mixed",
        ...     threshold=0.8
        ... )
        >>> result = validator_with_threshold.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return f"The column '{self.column}' doesn't have values that are null."

    def __call__(self, frame: Frame) -> Frame:
        """Check if the values in a column are null."""
        return (
            frame.select(self.column)
            .filter(
                nw.col(self.column).is_null() == False,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
