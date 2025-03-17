from __future__ import annotations

from typing import Literal, NotRequired, TypedDict


class SummaryTypedDict(TypedDict):
    passed: bool | None
    validations: list[str] | str
    failed_validation: NotRequired[list[str]]


class ResultValidationTypedDict(TypedDict):
    status: str
    threshold_pass: NotRequired[bool]
    message: str
    failing_items: NotRequired[list[str | int | float]]
    failed_number: NotRequired[int]
    frame_row_number: NotRequired[int]
    threshold: NotRequired[float]
    failed_percentage: NotRequired[float]


class ValidationTypedDict(TypedDict):
    validation: str
    impact: Literal["high", "medium", "low"]
    timestamp: str
    column: str
    result: ResultValidationTypedDict


class ResultsTypedDict(TypedDict):
    Summary: SummaryTypedDict
