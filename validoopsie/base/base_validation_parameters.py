from abc import abstractmethod
from typing import Literal, Optional

from narwhals.typing import IntoFrame


class BaseValidationParameters:
    """Base class for validation parameters."""

    def __init__(
        self,
        column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: Optional[float] = 0.00,
        **kwargs: object,
    ) -> None:
        self.column = column
        self.impact = impact.lower() if impact else impact
        self.threshold = threshold if threshold else 0.00
        self.__dict__.update(kwargs)

    @property
    @abstractmethod
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""

    @abstractmethod
    def __execute_check__(
        self,
        frame: IntoFrame,
    ) -> dict:
        """Execute the validation check on the provided frame."""
