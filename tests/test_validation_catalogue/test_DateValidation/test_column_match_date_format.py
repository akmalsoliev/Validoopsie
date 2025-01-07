from __future__ import annotations

import pendulum
from narwhals.typing import IntoDataFrame

from tests.utils import create_frame_fixture
from validoopsie.validation_catalogue.DateValidation import ColumnMatchDateFormat


@create_frame_fixture
def dataframe() -> dict[str, list]:
    start = pendulum.datetime(2021, 1, 1)
    end = pendulum.datetime(2021, 1, 20)
    interval = pendulum.Interval(start, end)
    list_interval = [date.to_date_string() for date in interval.range("days")]
    return {
        "dates_column": list_interval,
    }


def test_column_match_date_format(dataframe: IntoDataFrame) -> None:
    ds = ColumnMatchDateFormat("dates_column", date_format="YYYY-mm-dd")
    result = ds.__execute_check__(frame=dataframe)
    assert result["result"]["status"] == "Success"


@create_frame_fixture
def fail_dataframe() -> IntoDataFrame:
    return {
        "dates_column": ["2022-01-01", "2022-01-02", "2022-01-03", "2024/12/12"],
    }


def test_column_match_date_format_fail(fail_dataframe: IntoDataFrame) -> None:
    ds = ColumnMatchDateFormat(column="dates_column", date_format="YYYY-mm-dd")
    result = ds.__execute_check__(frame=fail_dataframe)
    assert result["result"]["status"] == "Fail"


def test_column_match_date_format_success_threshold(
    fail_dataframe: IntoDataFrame,
) -> None:
    ds = ColumnMatchDateFormat(
        column="dates_column",
        date_format="YYYY-mm-dd",
        threshold=0.5,
    )
    result = ds.__execute_check__(frame=fail_dataframe)
    assert result["result"]["status"] == "Success"


def test_column_match_date_format_fail_threshold(
    fail_dataframe: IntoDataFrame,
) -> None:
    ds = ColumnMatchDateFormat(
        column="dates_column",
        date_format="YYYY-mm-dd",
        threshold=0.1,
    )
    result = ds.__execute_check__(frame=fail_dataframe)
    assert result["result"]["status"] == "Fail"
