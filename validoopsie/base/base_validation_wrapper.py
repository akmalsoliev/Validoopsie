from __future__ import annotations

from datetime import datetime as dt
from datetime import timezone
from typing import TYPE_CHECKING, Any, TypeVar

import narwhals as nw
from loguru import logger
from narwhals.typing import IntoFrame

if TYPE_CHECKING:
    from validoopsie.types import KwargsType

T = TypeVar("T")


def get_items(
    nw_frame: IntoFrame,
    column: str,
) -> list[str | int | float]:
    if isinstance(nw_frame, nw.LazyFrame):
        return (
            nw_frame.select(nw.col(column).unique())
            .collect()
            .get_column(column)
            .sort()
            .to_list()
        )
    if isinstance(nw_frame, nw.DataFrame):
        return nw_frame.get_column(column).sort().unique().to_list()
    msg = (
        f"The frame is not a valid type. {type(nw_frame)}, if "
        "you reached this point please open an issue."
    )
    raise TypeError(msg)


def get_length(nw_frame: IntoFrame) -> int:
    if isinstance(nw_frame, nw.LazyFrame):
        return nw.to_py_scalar(nw_frame.select(nw.len()).collect().item())
    if isinstance(nw_frame, nw.DataFrame):
        return nw.to_py_scalar(nw_frame.select(nw.len()).item())
    msg = (
        f"The frame is not a valid type. {type(nw_frame)}, if "
        "you reached this point please open an issue."
    )
    raise TypeError(msg)


def get_count(nw_input_frame: nw.DataFrame, column: str) -> int:
    return nw.to_py_scalar(
        nw_input_frame.select(nw.col(f"{column}-count").sum()).item(),
    )


def log_exception_summary(class_name: str, name: str, error_str: str) -> None:
    fail_msg = f"An error occurred while validating {class_name}:\n{name} - {error_str!s}"
    logger.error(fail_msg)


def build_error_message(
    class_name: str,
    impact: str,
    column: str,
    error_str: str,
    current_time_str: str,
) -> dict[str, str | dict[str, str]]:
    return {
        "validation": class_name,
        "impact": impact,
        "timestamp": current_time_str,
        "column": column,
        "result": {
            "status": "Fail",
            "message": f"ERROR: {error_str!s}",
        },
    }


def check__impact(impact: str) -> None:
    fail_message: str = "Argument 'impact' is required."
    assert impact.lower() in ["low", "medium", "high"], fail_message


def check__threshold(threshold: float) -> None:
    fail_message: str = "Argument 'threshold' should be between 0 and 1."
    assert 0 <= threshold <= 1, fail_message


def get_frame(self: type, frame: IntoFrame) -> nw.DataFrame:
    validated_frame = self(frame)
    if isinstance(validated_frame, nw.LazyFrame):
        return validated_frame.collect()
    return validated_frame


def base_validation_wrapper(
    cls: type[T],
) -> type[T]:
    class Wrapper(cls):
        def __init__(
            self,
            *args: list[object],
            **kwargs: KwargsType,
        ) -> None:
            super().__init__(*args, **kwargs)
            self.column: str
            self.impact: str
            self.threshold: float
            self.fail_message: str
            check__impact(self.impact)
            check__threshold(self.threshold)

        def __execute_check__(
            self,
            frame: IntoFrame,
        ) -> dict[str, str | dict[str, Any]]:
            current_time_str = dt.now(tz=timezone.utc).astimezone().isoformat()
            try:
                frame = nw.from_native(frame)
                validated_frame = get_frame(self, frame)
                og_frame_rows_number: int = get_length(frame)
                vf_count_number: int = get_count(validated_frame, self.column)
                vf_row_number: int = get_length(validated_frame)
            except Exception as e:
                class_name = cls.__name__
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
                items: list[str | int | float] = get_items(validated_frame, self.column)
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
                "validation": str(cls.__name__),
                "impact": self.impact,
                "timestamp": current_time_str,
                "column": self.column,
                **result,
            }

    Wrapper.__name__ = cls.__name__
    Wrapper.__doc__ = cls.__doc__
    return Wrapper
