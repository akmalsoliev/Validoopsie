from __future__ import annotations

import pytest
from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.StringValidation import NotPatternMatch


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "codes": ["ABC001", "ABC002", "DEF001", "XYZ999", "LMNO12"],
        "codes2": ["BC001", "BC002", "DEF001", "XYZ999", "LMNO12"],
    }


# Unit Tests
def test_column_values_to_match_pattern_fail(sample_data: Frame) -> None:
    ds = NotPatternMatch("codes2", pattern="ABC")
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_column_values_to_match_pattern_success(sample_data: Frame) -> None:
    ds = NotPatternMatch("codes", pattern="^[A-Z]+[0-9]+$")
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_column_values_to_match_pattern_fail_threshold(sample_data: Frame) -> None:
    ds = NotPatternMatch("codes", pattern="ABC")
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_column_values_to_match_pattern_success_threshold(
    sample_data: Frame,
) -> None:
    ds = NotPatternMatch("codes", pattern="ABC", threshold=0.01)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


# Integration Tests
def test_column_values_to_match_pattern_fail_integration(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.NotPatternMatch("codes2", pattern="ABC")
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_column_values_to_match_pattern_success_integration(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.NotPatternMatch("codes", pattern="^[A-Z]+[0-9]+$", impact="high")
    with pytest.raises(ValueError):
        vd.validate()


def test_column_values_to_match_pattern_fail_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.NotPatternMatch("codes", pattern="ABC")
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"


def test_column_values_to_match_pattern_success_threshold_integration(
    sample_data: Frame,
) -> None:
    vd = Validate(sample_data)
    vd.StringValidation.NotPatternMatch(
        "codes",
        pattern="ABC",
        threshold=0.01,
    )
    result = vd.validate().results
    key = list(vd.results.keys())[1]
    assert result[key]["result"]["status"] == "Fail"
