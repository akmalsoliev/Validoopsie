import narwhals as nw
import polars as pl
import pytest
from narwhals.typing import IntoFrame

from tests.utils.create_frames import create_frame_fixture
from validoopsie.validation_catalogue.EqualityValidation import PairColumnEquality


@create_frame_fixture
def lf() -> IntoFrame:
    return {
        "A": [1, 2, 3, 4, 5],
        "B": [1, 2, 3, 4, 5],
        "C": [1, 2, 6, 4, 5],
    }


def test_pair_column_equlity_fail_one(lf: IntoFrame) -> None:
    test = PairColumnEquality(column="A", target_column="B")
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"
    assert result["result"]["threshold pass"] == True


def test_pair_column_equlity_fail_all(lf: IntoFrame) -> None:
    test = PairColumnEquality(column="A", target_column="C")
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_pair_column_equlity_fail_impact(lf: IntoFrame) -> None:
    test = PairColumnEquality(column="A", target_column="C", impact="high")
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"
    assert result["impact"] == "high"


def test_pair_column_equlity_fail_threshold(lf: IntoFrame) -> None:
    test = PairColumnEquality(column="A", target_column="C", threshold=0.0)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"


def test_pair_column_equlity_success_threshold(lf: IntoFrame) -> None:
    test = PairColumnEquality(column="A", target_column="C", threshold=0.4)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Success"
