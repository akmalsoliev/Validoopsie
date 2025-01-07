from __future__ import annotations

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


def test_vd_initialization(sample_data: ReturnT) -> None:
    vd = Validate(frame=sample_data)
    assert vd.results["Summary"]["passed"] is None
    assert vd.results["Summary"]["validations"] == "No validation checks were added."


def test_vd_result(sample_data: ReturnT) -> None:
    vd = Validate(frame=sample_data)
    test1_col = "column1"
    test2_col = "column2"
    vd.ValuesValidation.ColumnValuesToBeBetween(
        test1_col,
        1,
        5,
    ).ValuesValidation.ColumnUniqueValuesToBeInList(
        column=test2_col,
        values=["a", "b", "c", "d", "e"],
    )
    results = vd.results
    assert f"ColumnValuesToBeBetween_{test1_col}" in results
    assert f"ColumnUniqueValuesToBeInList_{test2_col}" in results


def test_vd_validation(sample_data: ReturnT) -> None:
    vd = Validate(frame=sample_data)
    vd.ValuesValidation.ColumnUniqueValuesToBeInList(
        column="column2",
        values=["a", "b", "c", "d"],
        impact="high",
    ).ValuesValidation.ColumnValuesToBeBetween(
        column="column1",
        min_value=1,
        max_value=2,
        impact="high",
    )
    with pytest.raises(SystemExit):
        vd.validate()


def test_validation_failure(sample_data: ReturnT) -> None:
    vd = Validate(sample_data)
    vd.ValuesValidation.ColumnUniqueValuesToBeInList(
        "column1",
        [1],
        impact="high",
    )
    with pytest.raises(SystemExit):
        vd.validate()


def test_no_validation_checks(sample_data: ReturnT) -> None:
    vd = Validate(sample_data)
    with pytest.raises(ValueError, match="No validation checks were added."):
        vd.validate()
