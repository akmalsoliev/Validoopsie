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


# Unit Tests
def test_string_length_to_be_between_fail(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test", min_value=1, max_value=4)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_string_length_to_be_between_fail_validation(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test", min_value=1, max_value=4, impact="high")


def test_string_length_to_be_between_fail_threshold(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test", min_value=1, max_value=4, threshold=0.6)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_string_length_to_be_between_success_threshold(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test", min_value=1, max_value=4, threshold=0.01)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_string_length_to_be_between_success(sample_data: Frame) -> None:
    ds = LengthToBeBetween("test2", min_value=1, max_value=5)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


# Integration Tests
def test_string_length_to_be_between_fail_integration(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test", min_value=1, max_value=4, impact="high")
    with pytest.raises(SystemExit):
        vd.validate()


def test_string_length_to_be_between_fail_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test", min_value=1, max_value=4, threshold=0.6)
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_string_length_to_be_between_success_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween(
        "test",
        min_value=1,
        max_value=4,
        threshold=0.01,
    )
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_string_length_to_be_between_success_integration(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeBetween("test2", min_value=1, max_value=5)
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"
