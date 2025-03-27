from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class LengthToBeEqualTo(BaseValidation):
    """Expect the column entries to be strings with length equal to `value`.

    Args:
        column (str): Column to validate.
        value (int): The expected value for a column entry length.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>>
        >>> # Validate fixed-length codes
        >>> df = pd.DataFrame({
        ...     "country_code": ["US", "UK", "FR"]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .StringValidation.LengthToBeEqualTo(
        ...         column="country_code",
        ...         value=2
        ...     )
        ... )
        >>> key = "LengthToBeEqualTo_country_code"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str,
        value: int,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
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
