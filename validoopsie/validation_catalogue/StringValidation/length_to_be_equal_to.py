from __future__ import annotations

from typing import Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class LengthToBeEqualTo(BaseValidation):
    """Expect the column entries to be strings with length equal to `value`.

    Parameters:
        column (str): Column to validate.
        value (int): The expected value for a column entry length.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> df = pd.DataFrame({
        ...     "strings1": ["12345", "abcde", "1b3d5", "1234", "4321"],
        ...     "strings2": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE"]
        ... })
        >>> frame = nw.from_native(df)

        >>> # Failing case - some strings do not have the expected length
        >>> validator = LengthToBeEqualTo("strings1", value=5)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # Success case - all strings have the expected length
        >>> validator = LengthToBeEqualTo("strings2", value=5)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # With threshold allowing some failures
        >>> validator_with_threshold = LengthToBeEqualTo(
        ...     column="strings1",
        ...     value=5,
        ...     threshold=0.6
        ... )
        >>> result = validator_with_threshold.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str,
        value: int,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)
        self.value = value

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        return (
            f"The column '{self.column}' has entries with length not "
            f"equal to {self.value}."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Expect the column entries to be strings with length equal to `value`."""
        return (
            frame.filter(
                nw.col(self.column).str.len_chars() != self.value,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
