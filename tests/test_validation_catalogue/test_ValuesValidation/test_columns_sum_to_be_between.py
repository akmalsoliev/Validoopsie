from __future__ import annotations

import pytest
from narwhals.typing import IntoFrame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.ValuesValidation import ColumnsSumToBeBetween


@create_frame_fixture
def lf() -> dict[str, list]:
    return {
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1],
        "C": [1.0, 2.0, 3.0, 4.0, 5.0],
        "D": [5, 4, 3, 2, 0],
        "E": ["1", "2", "3", "4", "5"],
    }


# Unit Tests for Greater Than (min_sum_value only)
def test_columns_sum_to_be_greater_than_fail(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "B"], min_sum_value=25)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_columns_sum_to_be_greater_than_success(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "B"], min_sum_value=6)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


# Unit Tests for Less Than (max_sum_value only)
def test_columns_sum_to_be_less_than_fail(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "B"], max_sum_value=7)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


def test_columns_sum_to_be_less_than_success(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "B"], max_sum_value=30)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


# Unit Tests for Between (min_sum_value and max_sum_value)
def test_columns_sum_to_be_between_fail(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "B"], min_sum_value=10, max_sum_value=15)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_columns_sum_to_be_between_success(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "B"], min_sum_value=3, max_sum_value=10)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


# Unit Tests with Threshold
def test_columns_sum_to_be_with_threshold_fail(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "D"], min_sum_value=25, threshold=0.1)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_columns_sum_to_be_with_threshold_success(lf: IntoFrame) -> None:
    test = ColumnsSumToBeBetween(["A", "D"], min_sum_value=6, threshold=0.5)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"
    assert result["result"]["threshold pass"] is True


# Integration Tests for Greater Than (min_sum_value only)
def test_columns_sum_to_be_greater_than_fail_integration(lf: IntoFrame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnsSumToBeBetween(["A", "B"], min_sum_value=25, impact="high")
    with pytest.raises(ValueError):
        vd.validate()


def test_columns_sum_to_be_greater_than_success_integration(lf: IntoFrame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnsSumToBeBetween(["A", "B"], min_sum_value=6)
    result = vd.validate().results
    key = list(result.keys())[1]
    assert result[key]["result"]["status"] == "Success"


# Integration Tests for Less Than (max_sum_value only)
def test_columns_sum_to_be_less_than_fail_integration(lf: IntoFrame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnsSumToBeBetween(["A", "B"], max_sum_value=7, impact="high")
    vd.validate()


def test_columns_sum_to_be_less_than_success_integration(lf: IntoFrame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnsSumToBeBetween(["A", "B"], max_sum_value=30)
    result = vd.validate().results
    key = list(result.keys())[1]
    assert result[key]["result"]["status"] == "Success"


# Integration Tests for Between (min_sum_value and max_sum_value)
def test_columns_sum_to_be_between_fail_integration(lf: IntoFrame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnsSumToBeBetween(
        ["A", "B"],
        min_sum_value=10,
        max_sum_value=15,
        impact="high",
    )
    with pytest.raises(ValueError):
        vd.validate()


def test_columns_sum_to_be_between_success_integration(lf: IntoFrame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnsSumToBeBetween(
        ["A", "B"],
        min_sum_value=3,
        max_sum_value=10,
    )
    result = vd.validate().results
    key = list(result.keys())[1]
    assert result[key]["result"]["status"] == "Success"
