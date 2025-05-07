from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import narwhals as nw
from loguru import logger
from narwhals.dataframe import DataFrame
from narwhals.typing import IntoFrame

from validoopsie.base.results_typedict import (
    ResultValidationTypedDict,
    ValidationTypedDict,
)


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
    result: int | None = None
    if isinstance(nw_frame, nw.LazyFrame):
        result = int(nw.to_py_scalar(nw_frame.select(nw.len()).collect().item()))
    if isinstance(nw_frame, nw.DataFrame):
        result = int(nw.to_py_scalar(nw_frame.select(nw.len()).item()))

    assert isinstance(result, int), "The result is not an integer. Method: get_length"
    return result


def get_count(nw_input_frame: DataFrame[Any], column: str) -> int:
    result = int(
        nw.to_py_scalar(
            nw_input_frame.select(nw.col(f"{column}-count").sum()).item(),
        ),
    )

    assert isinstance(result, int), "The result is not an integer. Method: get_count"
    return result


def log_exception_summary(class_name: str, name: str, error_str: str) -> None:
    fail_msg = f"An error occurred while validating {class_name}:\n{name} - {error_str!s}"
    logger.error(fail_msg)


def build_error_message(
    class_name: str,
    impact: Literal["low", "medium", "high"],
    column: str,
    error_str: str,
    current_time_str: str,
) -> ValidationTypedDict:
    failed_dict = ResultValidationTypedDict(
        status="Fail",
        message=f"ERROR: {error_str!s}",
    )

    return ValidationTypedDict(
        validation=class_name,
        impact=impact,
        timestamp=current_time_str,
        column=column,
        result=failed_dict,
    )


def check__impact(impact: str) -> None:
    fail_message: str = "Argument 'impact' is required."
    assert impact.lower() in ["low", "medium", "high"], fail_message


def check__threshold(threshold: float) -> None:
    fail_message: str = "Argument 'threshold' should be between 0 and 1."
    assert 0 <= threshold <= 1, fail_message


def collect_frame(frame: IntoFrame) -> DataFrame[Any]:
    if isinstance(frame, nw.LazyFrame):
        return frame.collect()
    error_msg = "The frame is not a valid type."
    assert isinstance(frame, nw.DataFrame), error_msg
    return frame
