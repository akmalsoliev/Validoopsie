from __future__ import annotations

from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie.validation_catalogue.ValuesValidation import ColumnUniqueValuesToBeInList


@create_frame_fixture
def sample_data() -> dict[str, list]:
    berlin = ["Berlin" for _ in range(4)]
    rome = ["Rome" for _ in range(5)]
    return {
        "cities": berlin + rome + ["Paris"],
    }


def test_column_unique_values_to_be_in_list_fail(sample_data: Frame) -> None:
    ds = ColumnUniqueValuesToBeInList("cities", ["Berlin", "Rome"])
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_column_unique_values_to_be_in_list_fail_threshold(sample_data: Frame) -> None:
    ds = ColumnUniqueValuesToBeInList("cities", ["Berlin", "Rome"], threshold=0.5)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_column_unique_values_to_be_in_list_success_threshold(sample_data: Frame) -> None:
    ds = ColumnUniqueValuesToBeInList("cities", ["Berlin", "Rome"], threshold=0.01)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_column_unique_values_to_be_in_list_success(sample_data: Frame) -> None:
    ds = ColumnUniqueValuesToBeInList(
        column="cities",
        values=["Paris", "Rome", "Berlin"],
    )
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"
