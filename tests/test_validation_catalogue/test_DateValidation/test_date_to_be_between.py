from __future__ import annotations

from datetime import date, datetime

import pytest
from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.DateValidation import (
    DateToBeBetween,
)


@create_frame_fixture
def sample_date_data() -> dict[str, list]:
    return {
        "dates": [
            date(2023, 1, 1),
            date(2023, 2, 15),
            date(2023, 3, 30),
            date(2023, 4, 1),
            date(2023, 5, 15),
        ],
        "dates2": [
            datetime(2023, 6, 1),
            datetime(2023, 7, 15),
            datetime(2023, 8, 30),
            datetime(2023, 9, 1),
            datetime(2023, 10, 15),
        ],
    }


# Unit Tests for DateToBeBetween
def test_date_to_be_between_fail(sample_date_data: Frame) -> None:
    ds = DateToBeBetween("dates", min_date=date(2023, 2, 1), max_date=date(2023, 4, 30))
    result = ds.__execute_check__(frame=sample_date_data)
    assert result["result"]["status"] == "Fail"


def test_date_to_be_between_fail_validation(sample_date_data: Frame) -> None:
    vd = Validate(sample_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        min_date=date(2023, 2, 1),
        max_date=date(2023, 4, 30),
        impact="high",
    )


def test_date_to_be_between_success_with_threshold(sample_date_data: Frame) -> None:
    ds = DateToBeBetween(
        "dates",
        min_date=date(2023, 2, 1),
        max_date=date(2023, 4, 30),
        threshold=0.6,
    )
    result = ds.__execute_check__(frame=sample_date_data)
    assert result["result"]["status"] == "Success"


def test_date_to_be_between_fail_with_low_threshold(sample_date_data: Frame) -> None:
    ds = DateToBeBetween(
        "dates",
        min_date=date(2023, 2, 1),
        max_date=date(2023, 4, 30),
        threshold=0.01,
    )
    result = ds.__execute_check__(frame=sample_date_data)
    assert result["result"]["status"] == "Fail"

def test_date_to_be_between_success(sample_date_data: Frame) -> None:
    ds = DateToBeBetween(
        "dates2",
        min_date=datetime(2023, 6, 1),
        max_date=datetime(2023, 10, 15),
    )
    result = ds.__execute_check__(frame=sample_date_data)
    assert result["result"]["status"] == "Success"


# Integration Tests for DateToBeBetween
def test_date_to_be_between_fail_integration(sample_date_data: Frame) -> None:
    vd = Validate(sample_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        min_date=date(2023, 2, 1),
        max_date=date(2023, 4, 30),
        impact="high",
    )
    with pytest.raises(ValueError):
        vd.validate()


def test_date_to_be_between_success_with_threshold_integration(
    sample_date_data: Frame,
) -> None:
    vd = Validate(sample_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        min_date=date(2023, 2, 1),
        max_date=date(2023, 4, 30),
        threshold=0.6,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_date_to_be_between_fail_with_low_threshold_integration(
    sample_date_data: Frame,
) -> None:
    vd = Validate(sample_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        min_date=date(2023, 2, 1),
        max_date=date(2023, 4, 30),
        threshold=0.01,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_date_to_be_between_success_integration(sample_date_data: Frame) -> None:
    vd = Validate(sample_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates2",
        min_date=datetime(2023, 6, 1),
        max_date=datetime(2023, 10, 15),
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


@create_frame_fixture
def less_date_data() -> dict[str, list]:
    return {
        "dates": [
            date(2023, 1, 1),
            date(2023, 2, 15),
            date(2023, 3, 30),
            date(2023, 4, 1),
            date(2023, 5, 15),
        ],
    }


# Unit Tests for Min Date Validation with Less Data
def test_min_date_to_be_between_fail(less_date_data: Frame) -> None:
    ds = DateToBeBetween("dates", min_date=date(2023, 6, 1))
    result = ds.__execute_check__(frame=less_date_data)
    assert result["result"]["status"] == "Fail"


def test_min_date_to_be_between_success_with_threshold(less_date_data: Frame) -> None:
    ds = DateToBeBetween("dates", min_date=date(2023, 3, 1), threshold=0.5)
    result = ds.__execute_check__(frame=less_date_data)
    assert result["result"]["status"] == "Success"


def test_min_date_to_be_between_fail_with_low_threshold(less_date_data: Frame) -> None:
    ds = DateToBeBetween("dates", min_date=date(2023, 6, 1), threshold=0.1)
    result = ds.__execute_check__(frame=less_date_data)
    assert result["result"]["status"] == "Fail"


def test_min_date_to_be_between_success(less_date_data: Frame) -> None:
    ds = DateToBeBetween("dates", min_date=date(2023, 1, 1))
    result = ds.__execute_check__(frame=less_date_data)
    assert result["result"]["status"] == "Success"


# Integration Tests for Min Date Validation with Less Data
def test_min_date_to_be_between_fail_integration(less_date_data: Frame) -> None:
    vd = Validate(less_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        min_date=date(2023, 6, 1),
        impact="high",
    )
    with pytest.raises(ValueError):
        vd.validate()


def test_min_date_to_be_between_success_with_threshold_integration(
    less_date_data: Frame,
) -> None:
    vd = Validate(less_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        min_date=date(2023, 3, 1),
        threshold=0.5,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_min_date_to_be_between_fail_with_low_threshold_integration(
    less_date_data: Frame,
) -> None:
    vd = Validate(less_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        min_date=date(2023, 6, 1),
        threshold=0.1,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_min_date_to_be_between_success_integration(less_date_data: Frame) -> None:
    vd = Validate(less_date_data)
    vd.DateValidation.DateToBeBetween("dates", min_date=date(2023, 1, 1))
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


@create_frame_fixture
def greater_date_data() -> dict[str, list]:
    return {
        "dates": [
            date(2023, 1, 1),
            date(2023, 2, 15),
            date(2023, 3, 30),
            date(2023, 4, 1),
            date(2023, 5, 15),
        ],
        "dates2": [
            datetime(2023, 6, 1),
            datetime(2023, 7, 15),
            datetime(2023, 8, 30),
            datetime(2023, 9, 1),
            datetime(2023, 10, 15),
        ],
    }


# Unit Tests
def test_date_to_be_less_than_or_equal_to_fail(greater_date_data: Frame) -> None:
    ds = DateToBeBetween("dates", max_date=date(2023, 4, 30))
    result = ds.__execute_check__(frame=greater_date_data)
    assert result["result"]["status"] == "Fail"


def test_date_to_be_less_than_or_equal_to_fail_threshold(
    greater_date_data: Frame,
) -> None:
    ds = DateToBeBetween(
        "dates2",
        max_date=datetime(2023, 9, 1),
        threshold=0.5,
    )
    result = ds.__execute_check__(frame=greater_date_data)
    assert result["result"]["status"] == "Success"


def test_date_to_be_less_than_or_equal_to_success_threshold(
    greater_date_data: Frame,
) -> None:
    ds = DateToBeBetween("dates", max_date=date(2023, 4, 30), threshold=0.1)
    result = ds.__execute_check__(frame=greater_date_data)
    assert result["result"]["status"] == "Fail"


def test_date_to_be_less_than_or_equal_to_success(greater_date_data: Frame) -> None:
    ds = DateToBeBetween("dates", max_date=date(2023, 12, 31))
    result = ds.__execute_check__(frame=greater_date_data)
    assert result["result"]["status"] == "Success"


# Integration Tests
def test_date_to_be_less_than_or_equal_to_fail_integration(
    greater_date_data: Frame,
) -> None:
    vd = Validate(greater_date_data)
    vd.DateValidation.DateToBeBetween("dates", max_date=date(2023, 4, 30), impact="high")
    with pytest.raises(ValueError):
        vd.validate()


def test_date_to_be_less_than_or_equal_to_fail_threshold_integration(
    greater_date_data: Frame,
) -> None:
    vd = Validate(greater_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates2",
        max_date=datetime(2023, 9, 1),
        threshold=0.5,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_date_to_be_less_than_or_equal_to_success_threshold_integration(
    greater_date_data: Frame,
) -> None:
    vd = Validate(greater_date_data)
    vd.DateValidation.DateToBeBetween(
        "dates",
        max_date=date(2023, 4, 30),
        threshold=0.1,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_date_to_be_less_than_or_equal_to_success_integration(
    greater_date_data: Frame,
) -> None:
    vd = Validate(greater_date_data)
    vd.DateValidation.DateToBeBetween("dates", max_date=date(2023, 12, 31))
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"
