from __future__ import annotations

from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie.validation_catalogue.ValuesValidation import ColumnValuesToBeBetween


@create_frame_fixture
def lf() -> dict[str, list]:
    return {
        "A": [1, 2, 3, 4, 5],
        "B": [1.0, 2.0, 3.0, 4.0, 5.0],
    }


def test_except_column_values_to_be_between(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 2)
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_except_column_values_to_be_between_threshold(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 2, threshold=0.5)
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_except_column_values_to_be_between_success_threshold(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 2, threshold=0.6)
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Success"


def test_except_column_values_to_be_between_success(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 5)
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Success"
