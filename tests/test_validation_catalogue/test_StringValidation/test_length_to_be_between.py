from __future__ import annotations

import pytest
from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.StringValidation import (
    LengthToBeBetween,
)


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "test": ["12345", "abcde", "1b3d5", "1234", "4321"],
        "test2": ["A", "13579", "24680", "12345", "abcde"],
    }


# Unit Tests for LengthToBeBetween
def test_length_to_be_between_fail(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test", min_value=1, max_value=4)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_length_to_be_between_fail_validation(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test", min_value=1, max_value=4, impact="high")


def test_length_to_be_between_success_with_threshold(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test", min_value=1, max_value=4, threshold=0.6)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_length_to_be_between_fail_with_low_threshold(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test", min_value=1, max_value=4, threshold=0.01)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_length_to_be_between_success(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test2", 1, 5)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


# Integration Tests for LengthToBeBetween
def test_length_to_be_between_fail_integration(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test", min_value=1, max_value=4, impact="high")
    with pytest.raises(ValueError):
        vd.validate()


def test_length_to_be_between_success_with_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test", min_value=1, max_value=4, threshold=0.6)
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_length_to_be_between_fail_with_low_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween(
        "test",
        min_value=1,
        max_value=4,
        threshold=0.01,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_length_to_be_between_success_integration(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test2", min_value=1, max_value=5)
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


@create_frame_fixture
def less_data() -> dict[str, list]:
    return {
        "strings": ["apple", "banana", "cherry", "date", "elderberry"],
    }


# Unit Tests for Min Length Validation with Less Data
def test_min_length_to_be_between_fail(less_data: Frame) -> None:
    ds = LengthToBeBetween("strings", min_value=6)
    result = ds.__execute_check__(frame=less_data)
    assert result["result"]["status"] == "Fail"


def test_min_length_to_be_between_success_with_threshold(less_data: Frame) -> None:
    ds = LengthToBeBetween("strings", min_value=6, threshold=0.5)
    result = ds.__execute_check__(frame=less_data)
    assert result["result"]["status"] == "Success"


def test_min_length_to_be_between_fail_with_low_threshold(less_data: Frame) -> None:
    ds = LengthToBeBetween("strings", min_value=6, threshold=0.1)
    result = ds.__execute_check__(frame=less_data)
    assert result["result"]["status"] == "Fail"


def test_min_length_to_be_between_success(less_data: Frame) -> None:
    ds = LengthToBeBetween("strings", min_value=4)
    result = ds.__execute_check__(frame=less_data)
    assert result["result"]["status"] == "Success"


# Integration Tests for Min Length Validation with Less Data
def test_min_length_to_be_between_fail_integration(less_data: Frame) -> None:
    vd = Validate(less_data)
    vd.StringValidation.LengthToBeBetween(
        "strings",
        min_value=6,
        impact="high",
    )
    with pytest.raises(ValueError):
        vd.validate()


def test_min_length_to_be_between_success_with_threshold_integration(
    less_data: Frame,
) -> None:
    vd = Validate(less_data)
    vd.StringValidation.LengthToBeBetween(
        "strings",
        min_value=6,
        threshold=0.5,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_min_length_to_be_between_fail_with_low_threshold_integration(
    less_data: Frame,
) -> None:
    vd = Validate(less_data)
    vd.StringValidation.LengthToBeBetween(
        "strings",
        min_value=6,
        threshold=0.1,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_min_length_to_be_between_success_integration(less_data: Frame) -> None:
    vd = Validate(less_data)
    vd.StringValidation.LengthToBeBetween("strings", min_value=4)
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


@create_frame_fixture
def greater_data() -> dict[str, list]:
    return {
        "strings": ["apple", "banana", "cherry", "date", "elderberry"],
        "strings2": ["hi", "hello", "how", "date", "when"],
    }


# Unit Tests
def test_string_length_to_be_less_than_or_equal_to_fail(greater_data: Frame) -> None:
    ds = LengthToBeBetween("strings", max_value=4)
    result = ds.__execute_check__(frame=greater_data)
    assert result["result"]["status"] == "Fail"


def test_string_length_to_be_less_than_or_equal_to_fail_threshold(
    greater_data: Frame,
) -> None:
    ds = LengthToBeBetween("strings2", max_value=4, threshold=0.5)
    result = ds.__execute_check__(frame=greater_data)
    assert result["result"]["status"] == "Success"


def test_string_length_to_be_less_than_or_equal_to_success_threshold(
    greater_data: Frame,
) -> None:
    ds = LengthToBeBetween("strings", max_value=4, threshold=0.1)
    result = ds.__execute_check__(frame=greater_data)
    assert result["result"]["status"] == "Fail"


def test_string_length_to_be_less_than_or_equal_to_success(greater_data: Frame) -> None:
    ds = LengthToBeBetween("strings", max_value=10)
    result = ds.__execute_check__(frame=greater_data)
    assert result["result"]["status"] == "Success"


# Integration Tests
def test_string_length_to_be_less_than_or_equal_to_fail_integration(
    greater_data: Frame,
) -> None:
    vd = Validate(greater_data)
    vd.StringValidation.LengthToBeBetween("strings", max_value=4, impact="high")
    with pytest.raises(ValueError):
        vd.validate()


def test_string_length_to_be_less_than_or_equal_to_fail_threshold_integration(
    greater_data: Frame,
) -> None:
    vd = Validate(greater_data)
    vd.StringValidation.LengthToBeBetween(
        "strings2",
        max_value=4,
        threshold=0.5,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_string_length_to_be_less_than_or_equal_to_success_threshold_integration(
    greater_data: Frame,
) -> None:
    vd = Validate(greater_data)
    vd.StringValidation.LengthToBeBetween(
        "strings",
        max_value=4,
        threshold=0.1,
    )
    result = vd.results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_string_length_to_be_less_than_or_equal_to_success_integration(
    greater_data: Frame,
) -> None:
    vd = Validate(greater_data)
    vd.StringValidation.LengthToBeBetween("strings", max_value=10)
    result = vd.results
    key = list(vd.results.keys())[1]
