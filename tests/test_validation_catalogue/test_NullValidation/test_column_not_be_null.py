from __future__ import annotations

from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie.validation_catalogue.NullValidation import ColumnNotBeNull


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "A": [1, 2, None, 4, 5],
        "B": [1.0, 2.0, 3.0, 4.0, 5.0],
        "C": [None for _ in range(5)],
    }


def test_except_column_values_to_not_be_null_fail(sample_data: Frame) -> None:
    test = ColumnNotBeNull(column="A")
    result = test.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_except_column_values_to_not_be_null_fail_5(sample_data: Frame) -> None:
    test = ColumnNotBeNull(column="C")
    result = test.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"
    assert result["result"]["failed_number"] == 5


def test_except_column_values_to_not_be_null_success(sample_data: Frame) -> None:
    test = ColumnNotBeNull(column="B")
    result = test.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"
