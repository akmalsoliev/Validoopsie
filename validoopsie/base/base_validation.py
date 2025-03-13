from __future__ import annotations

from abc import abstractmethod
from datetime import datetime as dt
from datetime import timezone
from typing import Any, Literal

import narwhals as nw
from narwhals.dataframe import DataFrame
from narwhals.typing import Frame, IntoFrame

from validoopsie.util.base_util_functions import (
    build_error_message,
    check__impact,
    check__threshold,
    collect_frame,
    get_count,
    get_items,
    get_length,
    log_exception_summary,
)


class BaseValidation:
    """Base class for validation parameters."""

    def __init__(
        self,
        column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        check__impact(impact)
        check__threshold(threshold)

        self.column = column
        # Sometimes operator can make a mistake and pass a string with a different case
        self.impact = impact.lower()
        self.threshold = threshold
        self.__dict__.update(kwargs)

        # This is mainly used for type checking validation
        self.schema_lenght: int | None = None

    @property
    @abstractmethod
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""

    @abstractmethod
    def __call__(self, frame: Frame) -> Frame:
        """Return the fail message, that will be used in the report."""

    @abstractmethod
    def __execute_check__(
        self,
        frame: IntoFrame,
    ) -> dict[str, Any]:
        """Execute the validation check on the provided frame."""
        current_time_str = dt.now(tz=timezone.utc).astimezone().isoformat()
        class_name = self.__class__.__name__
        try:
            # Just in case if the frame is not converted into Narwhals
            frame = nw.from_native(frame)

            # Execution of the validation
            validated_frame: Frame = self(frame)
            collected_frame: DataFrame[Any] = collect_frame(validated_frame)

            if self.schema_lenght is not None:
                og_frame_rows_number = self.schema_lenght
            else:
                og_frame_rows_number = get_length(frame)

            vf_row_number: int = get_length(collected_frame)
            vf_count_number: int = get_count(collected_frame, self.column)

        except Exception as e:
            name = type(e).__name__
            error_str = str(e)
            log_exception_summary(class_name, name, error_str)
            return build_error_message(
                class_name=class_name,
                impact=self.impact,
                column=self.column,
                error_str=error_str,
                current_time_str=current_time_str,
            )

        failed_percentage: float = (
            vf_count_number / og_frame_rows_number if vf_count_number > 0 else 0.00
        )
        threshold_pass: bool = failed_percentage <= self.threshold

        result = {}
        if vf_row_number > 0:
            items: list[str | int | float] = get_items(collected_frame, self.column)
            if not threshold_pass:
                result = {
                    "result": {
                        "status": "Fail",
                        "threshold pass": threshold_pass,
                        "message": self.fail_message,
                        "failing items": items,
                        "failed number": vf_count_number,
                        "frame row number": og_frame_rows_number,
                        "threshold": self.threshold,
                        "failed percentage": failed_percentage,
                    },
                }
            elif threshold_pass:
                result = {
                    "result": {
                        "status": "Success",
                        "threshold pass": threshold_pass,
                        "message": self.fail_message,
                        "failing items": items,
                        "failed number": vf_count_number,
                        "frame row number": og_frame_rows_number,
                        "threshold": self.threshold,
                        "failed percentage": failed_percentage,
                    },
                }

        else:
            result = {
                "result": {
                    "status": "Success",
                    "threshold pass": threshold_pass,
                    "message": "All items passed the validation.",
                    "frame row number": og_frame_rows_number,
                    "threshold": self.threshold,
                },
            }

        assert "result" in result, "The result key is missing."

        return {
            "validation": class_name,
            "impact": self.impact,
            "timestamp": current_time_str,
            "column": self.column,
            **result,
        }
