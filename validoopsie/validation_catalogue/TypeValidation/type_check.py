from __future__ import annotations

from typing import Literal

import narwhals as nw
import pyarrow as pa
from narwhals.dtypes import DType
from narwhals.typing import Frame

from validoopsie.base import BaseValidation


class TypeCheck(BaseValidation):
    """Validate the data type of the column(s).

    Parameters:
        column (str | None): The column to validate.
        column_type (type | None): The type of validation to perform.
        frame_schema_definition (dict[str, ValidoopsieType] | None): A dictionary of
            column names and their respective validation types.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> from narwhals.dtypes import Boolean, FloatType, IntegerType, String
        >>> df = pd.DataFrame({
        ...     "IntegerType": [1, -15, 32, 64, 128],
        ...     "FloatType": [1.23, -45.67, 0.01, 3.14159, 2.71828],
        ...     "String": ["hello", "world", "narwhals", "data", "type"],
        ...     "Boolean": [True, False, True, False, True]
        ... })
        >>> frame = nw.from_native(df)

        >>> # Success case - checking a single column with correct type
        >>> validator = TypeCheck(column="IntegerType", column_type=IntegerType)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Failing case - checking a single column with incorrect type
        >>> validator = TypeCheck(column="IntegerType", column_type=FloatType)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # Multiple column validation - all types correct
        >>> frame_schema_definition = {
        ...     "IntegerType": IntegerType,
        ...     "FloatType": FloatType,
        ...     "String": String,
        ...     "Boolean": Boolean,
        ... }
        >>> validator = TypeCheck(frame_schema_definition=frame_schema_definition)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'

        >>> # Multiple column validation - with errors
        >>> frame_schema_definition = {
        ...     "IntegerType": IntegerType,
        ...     "FloatType": FloatType,
        ...     "String": FloatType,  # Intentional error
        ...     "Boolean": Boolean
        ... }
        >>> validator = TypeCheck(frame_schema_definition=frame_schema_definition)
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Fail'

        >>> # With threshold allowing some failures
        >>> frame_schema_definition = {
        ...     "IntegerType": FloatType,  # Intentional error
        ...     "FloatType": FloatType,
        ...     "String": String,
        ...     "Boolean": Boolean,
        ... }
        >>> validator = TypeCheck(
        ...     frame_schema_definition=frame_schema_definition,
        ...     threshold=0.75
        ... )
        >>> result = validator.__execute_check__(frame=frame)
        >>> result["result"]["status"]
        'Success'
    """

    def __init__(
        self,
        column: str | None = None,
        column_type: type | None = None,
        frame_schema_definition: dict[str, type] | None = None,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: dict[str, object],
    ) -> None:
        # Single validation check
        if column and column_type:
            self.__check_validation_parameter__(column, column_type, DType)
            self.column_type = column_type
            self.frame_schema_definition = {column: column_type}

        # Multiple validation checks
        elif not column and not column_type and frame_schema_definition:
            # Check if Validation inside of the dictionary is actually correct
            for vcolumn, vtype in frame_schema_definition.items():
                self.__check_validation_parameter__(vcolumn, vtype, DType)

            column = "DataTypeColumnValidation"
            self.frame_schema_definition = frame_schema_definition
        else:
            error_message = (
                "Either `column` and `validation_type` should be provided or "
                "`frame_schema_definition` should be provided.",
            )
            raise ValueError(error_message)

        super().__init__(column, impact, threshold, **kwargs)

    def __check_validation_parameter__(
        self,
        column: str,
        column_type: type,
        expected_type: type,
    ) -> None:
        """Check if the validation parameter is correct."""
        if not issubclass(column_type, expected_type):
            error_message = (
                f"Validation type must be a subclass of DType, column: {column}, "
                f"type: {column_type.__name__}."
            )
            raise TypeError(error_message)

    @property
    def fail_message(self) -> str:
        """Return the fail message, that will be used in the report."""
        if self.column == "DataTypeColumnValidation":
            return (
                "The data type of the column(s) is not correct. "
                "Please check `column_type_definitions`."
            )

        return (
            f"The column '{self.column}' has failed the Validation, "
            f"expected type: {self.column_type}."
        )

    def __call__(self, frame: Frame) -> Frame:
        """Validate the data type of the column(s)."""
        schema = frame.schema
        # Introduction of a new structure where the schema len will be used a frame length
        self.schema_lenght = schema.len()
        failed_columns = []
        for column_name in self.frame_schema_definition:
            # Should this be raised or not?
            if column_name not in schema:
                failed_columns.append(column_name)
                continue

            column_type = schema[column_name]
            defined_type = self.frame_schema_definition[column_name]

            if not issubclass(column_type.__class__, defined_type):
                failed_columns.append(column_name)

        return nw.from_native(pa.table({self.column: failed_columns})).with_columns(
            nw.lit(1).alias(f"{self.column}-count"),
        )
