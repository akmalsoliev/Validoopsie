from __future__ import annotations

from narwhals.typing import IntoFrame

from tests.utils.create_frames import create_frame_fixture
from validoopsie.validation_catalogue.ValuesValidation import ColumnsSumToBeEqualTo


@create_frame_fixture
def lf() -> dict[str, list]:
    return {
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1],
        "C": [1.0, 2.0, 3.0, 4.0, 5.0],
        "D": [5, 4, 3, 2, 2],
        "E": ["1", "2", "3", "4", "5"],
    }


def test_fail_columns_sum_to_be_equal_to(lf: IntoFrame) -> None:
    test = ColumnsSumToBeEqualTo(["A", "B"], 6)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"


def test_fail_but_threshold_success_columns_sum_to_be_equal_to(lf: IntoFrame) -> None:
    test = ColumnsSumToBeEqualTo(["A", "D"], 6, threshold=0.5)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"
    assert result["result"]["threshold pass"] == True


def test_error_columns_sum_to_be_equal_to(lf: IntoFrame) -> None:
    test = ColumnsSumToBeEqualTo(["A", "E"], 6, threshold=0.5)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_fail_threshold_columns_sum_to_be_equal_to(lf: IntoFrame) -> None:
    test = ColumnsSumToBeEqualTo(["A", "D"], 6, threshold=0.1)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_high_impact_columns_sum_to_be_equal_to(lf: IntoFrame) -> None:
    test = ColumnsSumToBeEqualTo(["A", "D"], 6, threshold=0.1, impact="High")
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"
    assert result["impact"] == "high"
