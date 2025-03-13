from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest
from narwhals.dtypes import (
    Boolean,
    Date,
    Datetime,
    Duration,
    FloatType,
    Int64,
    IntegerType,
    List,
    String,
)
from narwhals.typing import Frame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.validation_catalogue.TypeValidation import TypeCheck


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "IntegerType": [
            1,
            -15,
            32,
            64,
            128,
        ],  # Example data for Int8, Int16, Int32, Int64, Int128
        "FloatType": [
            1.23,
            -45.67,
            0.01,
            3.14159,
            2.71828,
        ],  # Example data for Float32, Float64, Decimal
        "String": ["hello", "world", "narwhals", "data", "type"],  # Example strings
        "Boolean": [True, False, True, False, True],  # Example booleans
        "UIntegerType": [
            0,
            15,
            32,
            64,
            128,
        ],  # Example unsigned integers (UInt8, UInt16, UInt32, UInt64, UInt128)
        "CategoryType": ["A", "B", "C", "A", "B"],  # Example categorical data
        "ObjectType": [
            {"key1": "value1"},
            {"key2": "value2"},
            {},
            {"key3": "value3"},
            {"key4": "value4"},
        ],  # Example objects
        "EnumType": [
            "Red",
            "Green",
            "Blue",
            "Yellow",
            "Black",
        ],  # Example enumeration values
        "List": [[1, 2, 3], [4, 5], [], [6], [7, 8]],  # Example arrays/lists
        "Datetime": [
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 6, 15, 15, 30),
            datetime(2023, 12, 31, 23, 59),
            datetime(2024, 1, 1),
            datetime(2024, 11, 11, 11, 11),
        ],  # Example datetimes
        "Date": [
            date(2023, 1, 1),
            date(2023, 6, 15),
            date(2023, 12, 31),
            date(2024, 1, 1),
            date(2024, 11, 11),
        ],  # Example dates
        "Duration": [
            timedelta(days=1),  # Duration of 1 day
            timedelta(days=2),  # Duration of 2 days
            timedelta(days=3),  # Duration of 3 days
            timedelta(hours=4),  # Duration of 4 hours
            timedelta(minutes=5),  # Duration of 5 minutes
        ],  # Example durations
    }


# Unit Tests
def test_type_check_success_single_column(sample_data: Frame) -> None:
    ds = TypeCheck("IntegerType", IntegerType)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_type_check_success_single_column_specific_type(sample_data: Frame) -> None:
    ds = TypeCheck("IntegerType", Int64)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_type_check_failure_single_column(sample_data: Frame) -> None:
    ds = TypeCheck("IntegerType", FloatType)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


def test_date_check_success_single_column(
    sample_data: Frame,
    request: pytest.FixtureRequest,
) -> None:
    if request.node.callspec.id == "pandas":
        pytest.skip("Pandas does not support Date type")
    ds = TypeCheck("Date", Date)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_type_check_success_multiple_columns(sample_data: Frame) -> None:
    frame_schema_definition = {
        "IntegerType": IntegerType,
        "FloatType": FloatType,
        "String": String,
        "Boolean": Boolean,
    }
    ds = TypeCheck(frame_schema_definition=frame_schema_definition)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_type_check_failure_multiple_columns(sample_data: Frame) -> None:
    frame_schema_definition = {
        "IntegerType": IntegerType,
        "FloatType": FloatType,
        "String": FloatType,
    }
    ds = TypeCheck(None, None, frame_schema_definition=frame_schema_definition)
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"
    assert result["result"]["failing items"][0] == "String"


def test_type_check_threshold_success(sample_data: Frame) -> None:
    frame_schema_definition = {
        "IntegerType": IntegerType,
        "FloatType": FloatType,
        "String": String,
        "Boolean": Boolean,
        "Date": Date,
        "Duration": Duration,
        "List": List,
    }
    ds = TypeCheck(
        None,
        None,
        frame_schema_definition=frame_schema_definition,
        threshold=0.75,
    )
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Success"


def test_type_check_threshold_failure(sample_data: Frame) -> None:
    frame_schema_definition = {
        "IntegerType": FloatType,  # Intentional error
        "FloatType": String,  # Intentional error
        "String": FloatType,  # Intentional error
        "Boolean": Boolean,
    }
    ds = TypeCheck(
        None,
        None,
        frame_schema_definition=frame_schema_definition,
        threshold=0.20,  # only 20% of columns can fail
    )
    result = ds.__execute_check__(frame=sample_data)
    assert result["result"]["status"] == "Fail"


# Integration Tests


def test_type_check_integration_success(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.TypeValidation.TypeCheck("IntegerType", IntegerType)
    result = vd.results
    key = list(vd.results.keys())[-1]
    assert result[key]["result"]["status"] == "Success"


def test_type_check_integration_failure_high_impact(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.TypeValidation.TypeCheck("IntegerType", FloatType, impact="high")
    with pytest.raises(ValueError):
        vd.validate()


def test_type_check_integration_failure_low_impact(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    vd.TypeValidation.TypeCheck("IntegerType", FloatType, impact="low")
    result = vd.results
    key = list(vd.results.keys())[-1]
    assert result[key]["result"]["status"] == "Fail"


def test_type_check_integration_threshold_success(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    frame_schema_definition = {
        "IntegerType": IntegerType,
        "FloatType": FloatType,
        "Boolean": Boolean,
        "String": String,
        "Date": Date,
        "Duration": Duration,
    }
    vd.TypeValidation.TypeCheck(
        None,
        None,
        frame_schema_definition=frame_schema_definition,
        threshold=0.8,
    )
    result = vd.results
    key = list(vd.results.keys())[-1]
    assert result[key]["result"]["status"] == "Success"


def test_type_check_integration_threshold_failure(sample_data: Frame) -> None:
    vd = Validate(sample_data)
    frame_schema_definition = {
        "IntegerType": FloatType,  # Intentional error
        "FloatType": String,  # Intentional error
        "Boolean": Boolean,
        "String": FloatType,  # Intentional error
        "Date": Datetime,  # Intentional mismatch
    }
    vd.TypeValidation.TypeCheck(
        frame_schema_definition=frame_schema_definition,
        impact="high",
    )

    with pytest.raises(ValueError):
        vd.validate()
