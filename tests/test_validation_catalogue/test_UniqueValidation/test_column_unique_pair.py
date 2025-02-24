from __future__ import annotations

import pytest
from narwhals.typing import Frame, IntoFrame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.UniqueValidation import ColumnUniquePair


@create_frame_fixture
def lf() -> dict[str, list]:
    return {
        "first_name": ["John", "Jane", "John", "Alice", "Bob"],
        "last_name": ["Doe", "Smith", "Smith", "Johnson", "Wilson"],
        "age": [30, 25, 35, 28, 42],
        "city": ["NY", "LA", "NY", "Chicago", "Boston"],
    }


# Unit Tests
def test_unique_pair_fail(lf: IntoFrame) -> None:
    """Test when there are duplicate combinations."""
    test = ColumnUniquePair(["first_name", "city"])
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_unique_pair_success(lf: IntoFrame) -> None:
    """Test when all combinations are unique."""
    test = ColumnUniquePair(["first_name", "age"])
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


def test_unique_pair_multiple_columns(lf: IntoFrame) -> None:
    """Test with more than two columns."""
    test = ColumnUniquePair(["first_name", "last_name", "city"])
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


def test_unique_pair_single_column(lf: IntoFrame) -> None:
    """Test with a single column."""
    test = ColumnUniquePair(["first_name"])
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


# Integration Tests
def test_unique_pair_fail_integration(lf: IntoFrame) -> None:
    """Integration test for failing case."""
    vd = Validate(lf)
    vd.UniqueValidation.ColumnUniquePair(["first_name", "city"], impact="high")
    with pytest.raises(ValueError):
        vd.validate()


def test_unique_pair_success_integration(lf: IntoFrame) -> None:
    """Integration test for successful case."""
    vd = Validate(lf)
    vd.UniqueValidation.ColumnUniquePair(["first_name", "age"])
    result = vd.results
    key = list(result.keys())[1]
    assert result[key]["result"]["status"] == "Success"


def test_unique_pair_multiple_validations_integration(lf: IntoFrame) -> None:
    """Test multiple unique pair validations together."""
    vd = Validate(lf)
    vd.UniqueValidation.ColumnUniquePair(["first_name", "age"])
    vd.UniqueValidation.ColumnUniquePair(["first_name", "last_name", "city"])
    result = vd.results

    for key in result:
        if key == "Summary":
            continue
        assert result[key]["result"]["status"] == "Success"


# Edge Cases
def test_unique_pair_empty_column_list(lf: Frame) -> None:
    """Test with empty column list."""
    with pytest.raises(AssertionError):
        ColumnUniquePair([], impact="high").__execute_check__(lf)


@create_frame_fixture
def empty_frame() -> dict[str, list]:
    return {
        "first_name": [],
        "last_name": [],
    }


def test_unique_pair_empty_frame(
    empty_frame: IntoFrame,
) -> None:
    """Test with empty dataframe."""
    test = ColumnUniquePair(["first_name", "last_name"], impact="high")
    test.__execute_check__(frame=empty_frame)


def test_unique_pair_nonexistent_column(lf: IntoFrame) -> None:
    """Test with non-existent column."""
    vd = Validate(lf)
    vd.UniqueValidation.ColumnUniquePair(["first_name", "non_existent"], impact="high")
    with pytest.raises(ValueError, match="Failed Validation"):
        vd.validate()


def test_unique_pair_different_column_types(lf: IntoFrame) -> None:
    """Test combining columns of different types."""
    test = ColumnUniquePair(["first_name", "age"])
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"
