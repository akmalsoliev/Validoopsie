import sys
from collections.abc import Iterable
from typing import Any, Literal, TypedDict

from tabulate import TableFormat

# NotRequired is available in typing from Python 3.11+
if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired


class SummaryTypedDict(TypedDict):
    passed: bool | None
    validations: list[str] | str
    failed_validation: list[str]


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


class KwargsParams(TypedDict, total=False):
    column: str
    impact: Literal["high", "medium", "low"]
    threshold: float


class TabulateKwargs(TypedDict, total=False):
    tablefmt: str | TableFormat
    floatfmt: str | Iterable[str]
    intfmt: str | Iterable[str]
    numalign: str | None
    stralign: str | None
    missingval: str | Iterable[str]
    showindex: bool | str | Iterable[Any]
    disable_numparse: bool | Iterable[int]
    colalign: Iterable[str | None] | None
    maxcolwidths: int | Iterable[int | None] | None
    rowalign: str | Iterable[str] | None
    maxheadercolwidths: int | Iterable[int] | None
