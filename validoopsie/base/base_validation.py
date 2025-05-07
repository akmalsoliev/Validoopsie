from __future__ import annotations

from abc import abstractmethod
from datetime import datetime as dt
from datetime import timezone
from typing import TYPE_CHECKING, Any, Literal, cast

import narwhals as nw
from narwhals.dataframe import DataFrame
from narwhals.typing import Frame, IntoFrame

from validoopsie.base.results_typedict import (
    KwargsParams,
    ResultValidationTypedDict,
    ValidationTypedDict,
)
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
        **kwargs: KwargsParams,
    ) -> None:
        check__impact(impact)
        check__threshold(threshold)

        # Sometimes operator can make a mistake and pass a string with a different case
        impact_lower = cast("Literal['low', 'medium', 'high']", impact.lower())
        self.impact: Literal["low", "medium", "high"] = impact_lower

        self.column = column
        self.threshold = threshold
        self.__dict__.update(kwargs)

        # This is mainly used for type checking validation
        self.schema_length: int | None = None

    @property
    @abstractmethod
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""

    @abstractmethod
    def __call__(self, frame: Frame) -> Frame:
        """Return the fail message, that will be used in the report."""

    def __execute_check__(
        self,
        frame: IntoFrame,
    ) -> ValidationTypedDict:
        """Execute the validation check on the provided frame."""
        current_time_str = dt.now(tz=timezone.utc).astimezone().isoformat()
        class_name = self.__class__.__name__
        try:
            # Just in case if the frame is not converted into Narwhals
            frame = nw.from_native(frame)

            # Execution of the validation
            validated_frame: Frame = self(frame)
            collected_frame: DataFrame[Any] = collect_frame(validated_frame)

            if self.schema_length is not None:
                og_frame_rows_number = self.schema_length
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

        if vf_row_number > 0:
            items: list[str | int | float] = get_items(collected_frame, self.column)
            status: str = "Fail"
            if threshold_pass:
                status = "Success"

            result = ResultValidationTypedDict(
                status=status,
                threshold_pass=threshold_pass,
                message=self.fail_message,
                failing_items=items,
                failed_number=vf_count_number,
                frame_row_number=og_frame_rows_number,
                threshold=self.threshold,
                failed_percentage=failed_percentage,
            )

        else:
            result = ResultValidationTypedDict(
                status="Success",
                threshold_pass=threshold_pass,
                message="All items passed the validation.",
                frame_row_number=og_frame_rows_number,
                threshold=self.threshold,
            )

        return ValidationTypedDict(
            validation=class_name,
            impact=self.impact,
            timestamp=current_time_str,
            column=self.column,
            result=result,
        )
