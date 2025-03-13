from __future__ import annotations

import pytest
from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.UniqueValidation import (
    ColumnUniqueValueCountToBeBetween,
)


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "strings": ["A", "A", "A", "B", "B", "C", "D", "E"],
        "strings2": ["A", "B", "C", "D", "E", "F", "G", "H"],
    }


# Unit Tests for ColumnUniqueValueCountToBeBetween
def test_column_unique_value_count_to_be_between_fail(sample_data: Frame) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", max_value=2)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_column_unique_value_count_to_be_between_success(sample_data: Frame) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", min_value=1, max_value=3)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_column_unique_value_count_to_be_between_success_with_threshold(
    sample_data: Frame,
) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", max_value=2, threshold=0.6)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_column_unique_value_count_to_be_between_success_high_max_value(
    sample_data: Frame,
) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", max_value=10)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


# Unit Tests for Greater Than (min_value only)
def test_column_unique_value_count_greater_than_fail(sample_data: Frame) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", min_value=6)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_column_unique_value_count_greater_than_success(sample_data: Frame) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", min_value=1)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


# Unit Tests for Less Than (max_value only)
def test_column_unique_value_count_less_than_fail(sample_data: Frame) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", max_value=2)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_column_unique_value_count_less_than_success(sample_data: Frame) -> None:
    ds = ColumnUniqueValueCountToBeBetween("strings", max_value=5)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


# Integration Tests for ColumnUniqueValueCountToBeBetween
def test_column_unique_value_count_to_be_between_fail_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween(
        "strings",
        max_value=2,
        impact="high",
    )
    with pytest.raises(ValueError):
        vd.validate()


def test_column_unique_value_count_to_be_between_success_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween(
        "strings",
        min_value=1,
        max_value=3,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_column_unique_value_count_to_be_between_success_with_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween(
        "strings",
        max_value=2,
        threshold=0.6,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_column_unique_value_count_to_be_between_success_high_max_value_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween("strings", max_value=10)
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


# Integration Tests for Greater Than (min_value only)
def test_column_unique_value_count_greater_than_fail_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween(
        "strings",
        min_value=6,
        impact="high",
    )
    with pytest.raises(ValueError):
        vd.validate()


def test_column_unique_value_count_greater_than_success_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween("strings", min_value=1)
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


# Integration Tests for Less Than (max_value only)
def test_column_unique_value_count_less_than_fail_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween(
        "strings",
        max_value=2,
        impact="high",
    )
    with pytest.raises(ValueError):
        vd.validate()


def test_column_unique_value_count_less_than_success_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.UniqueValidation.ColumnUniqueValueCountToBeBetween("strings", max_value=5)
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"
