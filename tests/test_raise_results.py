from __future__ import annotations

import json
import re

import pytest

from tests.utils import ReturnT, create_frame_fixture
from validoopsie import Validate


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "column1": [1, 2, 3, 4, 5],
        "column2": ["a", "b", "c", "d", "e"],
        "column3": [10.5, 20.5, 30.5, 40.5, 50.5],
    }


def test_raise_results_default_behavior(sample_data: ReturnT) -> None:
    """Test that without raise_results=True."""
    vd = Validate(frame=sample_data)
    vd.ValuesValidation.ColumnValuesToBeBetween(
        column="column1",
        min_value=10,  # This will fail
        max_value=20,
        impact="high",
    )

    with pytest.raises(ValueError) as exc_info:
        vd.validate()

    error_message = str(exc_info.value)
    # Check that the error message contains the failed validation name
    assert "ColumnValuesToBeBetween_column1" in error_message
    # Check that the error message doesn't contain JSON formatting
    assert "{" not in error_message
    assert "}" not in error_message


def test_raise_results_true_includes_json(sample_data: ReturnT) -> None:
    """Test that with raise_results=True, error message includes JSON results."""
    vd = Validate(frame=sample_data)
    vd.ValuesValidation.ColumnValuesToBeBetween(
        column="column1",
        min_value=10,  # This will fail
        max_value=20,
        impact="high",
    )

    with pytest.raises(ValueError) as exc_info:
        vd.validate(raise_results=True)

    error_message = str(exc_info.value)
    # Check that the error message contains the failed validation name
    assert "ColumnValuesToBeBetween_column1" in error_message
    # Check that the error message contains JSON formatting
    assert "{" in error_message
    assert "}" in error_message

    # Extract the JSON part from the error message
    json_match = re.search(r"({.*})", error_message, re.DOTALL)
    assert json_match is not None

    # Verify that the extracted JSON is valid and contains expected data
    json_data = json.loads(json_match.group(1))
    assert "Summary" in json_data
    assert "ColumnValuesToBeBetween_column1" in json_data
    assert json_data["Summary"]["passed"] is False
    assert "ColumnValuesToBeBetween_column1" in json_data["Summary"]["failed_validation"]


def test_raise_results_with_multiple_failures(sample_data: ReturnT) -> None:
    """Test that with raise_results=True."""
    vd = Validate(frame=sample_data)
    vd.ValuesValidation.ColumnValuesToBeBetween(
        column="column1",
        min_value=10,  # This will fail
        max_value=20,
        impact="high",
    )
    vd.UniqueValidation.ColumnUniqueValuesToBeInList(
        column="column2",
        values=["x", "y", "z"],  # This will fail
        impact="high",
    )

    with pytest.raises(ValueError) as exc_info:
        vd.validate(raise_results=True)

    error_message = str(exc_info.value)

    # Extract the JSON part from the error message
    json_match = re.search(r"({.*})", error_message, re.DOTALL)
    assert json_match is not None

    # Verify that the extracted JSON is valid and contains both failures
    json_data = json.loads(json_match.group(1))
    assert "Summary" in json_data
    assert "ColumnValuesToBeBetween_column1" in json_data
    assert "ColumnUniqueValuesToBeInList_column2" in json_data
    assert len(json_data["Summary"]["failed_validation"]) == 2

    # Check that only the failed validations plus Summary are included
    assert len(json_data) == 3
