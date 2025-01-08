from __future__ import annotations

import pytest
from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.StringValidation import (
    LengthToBeLessThanOrEqualTo,
)


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "strings": ["apple", "banana", "cherry", "date", "elderberry"],
        "strings2": ["hi", "hello", "how", "date", "when"],
    }


# Unit Tests
def test_string_length_to_be_less_than_or_equal_to_fail(sample_data: Frame) -> None:
    ds = LengthToBeLessThanOrEqualTo("strings", max_value=4)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_string_length_to_be_less_than_or_equal_to_fail_threshold(
    sample_data: Frame,
) -> None:
    ds = LengthToBeLessThanOrEqualTo("strings2", max_value=4, threshold=0.5)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_string_length_to_be_less_than_or_equal_to_success_threshold(
    sample_data: Frame,
) -> None:
    ds = LengthToBeLessThanOrEqualTo("strings", max_value=4, threshold=0.1)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_string_length_to_be_less_than_or_equal_to_success(sample_data: Frame) -> None:
    ds = LengthToBeLessThanOrEqualTo("strings", max_value=10)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


# Integration Tests
def test_string_length_to_be_less_than_or_equal_to_fail_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeLessThanOrEqualTo("strings", max_value=4, impact="high")
    with pytest.raises(SystemExit):
        vd.validate()


def test_string_length_to_be_less_than_or_equal_to_fail_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeLessThanOrEqualTo(
        "strings2",
        max_value=4,
        threshold=0.5,
    )
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_string_length_to_be_less_than_or_equal_to_success_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeLessThanOrEqualTo(
        "strings",
        max_value=4,
        threshold=0.1,
    )
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_string_length_to_be_less_than_or_equal_to_success_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.LengthToBeLessThanOrEqualTo("strings", max_value=10)
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"
