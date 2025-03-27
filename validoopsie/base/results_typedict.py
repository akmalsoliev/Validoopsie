from __future__ import annotations

import sys
from typing import Literal, TypedDict

# NotRequired is available in typing from Python 3.11+
if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired


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


class KwargsParams(TypedDict, total=False):
    column: str
    impact: Literal["high", "medium", "low"]
    threshold: float
