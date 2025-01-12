from __future__ import annotations

import pytest
from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.ValuesValidation import ColumnValuesToBeBetween


@create_frame_fixture
def lf() -> dict[str, list]:
    return {
        "A": [1, 2, 3, 4, 5],
        "B": [1.0, 2.0, 3.0, 4.0, 5.0],
    }


# Unit Tests for ColumnValuesToBeBetween
def test_column_values_to_be_between_fail(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 2)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_column_values_to_be_between_fail_threshold(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 2, threshold=0.5)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_column_values_to_be_between_success_threshold(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 2, threshold=0.6)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


def test_column_values_to_be_between_success(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 5)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


# Unit Tests for Greater Than (min_value only)
def test_column_values_greater_than_fail(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", min_value=6)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_column_values_greater_than_success(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", min_value=1)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


# Unit Tests for Less Than (max_value only)
def test_column_values_less_than_fail(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", max_value=3)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_column_values_less_than_success(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", max_value=6)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


# Integration Tests for ColumnValuesToBeBetween
def test_column_values_to_be_between_fail_integration(lf: Frame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnValuesToBeBetween("A", 1, 2, impact="high")
    with pytest.raises(SystemExit):
        vd.validate()


def test_column_values_to_be_between_success_integration(lf: Frame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnValuesToBeBetween("A", 1, 5)
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_column_values_to_be_between_success_threshold_integration(lf: Frame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnValuesToBeBetween("A", 1, 2, threshold=0.6)
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


# Integration Tests for Greater Than (min_value only)
def test_column_values_greater_than_fail_integration(lf: Frame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnValuesToBeBetween("A", min_value=6, impact="high")
    with pytest.raises(SystemExit):
        vd.validate()


def test_column_values_greater_than_success_integration(lf: Frame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnValuesToBeBetween("A", min_value=1)
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


# Integration Tests for Less Than (max_value only)
def test_column_values_less_than_fail_integration(lf: Frame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnValuesToBeBetween("A", max_value=3, impact="high")
    with pytest.raises(SystemExit):
        vd.validate()


def test_column_values_less_than_success_integration(lf: Frame) -> None:
    vd = Validate(lf)
    vd.ValuesValidation.ColumnValuesToBeBetween("A", max_value=6)
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"
