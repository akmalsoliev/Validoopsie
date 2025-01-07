from __future__ import annotations

from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie.validation_catalogue.NullValidation import ColumnBeNull


@create_frame_fixture
def lf() -> dict[str, list]:
    return {
        "A": [1, 2, None, 4, 5],
        "B": [1.0, 2.0, 3.0, 4.0, 5.0],
        "C": [None for _ in range(5)],
    }


def test_column_be_null_fail(lf: Frame) -> None:
    test = ColumnBeNull(column="A")
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_column_be_null_fail_all(lf: Frame) -> None:
    test = ColumnBeNull(column="B")
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_column_be_null_pass(lf: Frame) -> None:
    test = ColumnBeNull(column="C", impact="medium")
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Success"
    assert result["impact"] == "medium"


def test_column_be_null_fail_threshold(lf: Frame) -> None:
    test = ColumnBeNull(column="A", threshold=0.1)
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_column_be_null_fail_threshold_impact_medium(lf: Frame) -> None:
    test = ColumnBeNull("A", threshold=0.1, impact="medium")
    result = test.execute_check(frame=lf)
    assert result["result"]["status"] == "Fail"
    assert result["impact"] == "medium"
