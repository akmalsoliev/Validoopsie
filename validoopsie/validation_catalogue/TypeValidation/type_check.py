from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import narwhals as nw
import pyarrow as pa
from narwhals.dtypes import DType
from narwhals.typing import Frame

from validoopsie.base import BaseValidation

if TYPE_CHECKING:
    from validoopsie.base.results_typedict import KwargsParams


class TypeCheck(BaseValidation):
    """Validate the data type of the column(s).

    Args:
        column (str | None): The column to validate.
        column_type (type | None): The type of validation to perform.
        frame_schema_definition (dict[str, type] | None): A dictionary
            of column names and their respective validation types.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".

    Examples:
        >>> import pandas as pd
        >>> from validoopsie import Validate
        >>> from narwhals.dtypes import IntegerType, FloatType, String
        >>>
        >>> # Validate column types
        >>> df = pd.DataFrame({
        ...     "id": [1001, 1002, 1003],
        ...     "name": ["Alice", "Bob", "Charlie"],
        ...     "balance": [100.50, 250.75, 0.00]
        ... })
        >>>
        >>> vd = (
        ...     Validate(df)
        ...     .TypeValidation.TypeCheck(
        ...         frame_schema_definition={
        ...             "id": IntegerType,
        ...             "name": String,
        ...             "balance": FloatType
        ...         }
        ...     )
        ... )
        >>>
        >>> key = "TypeCheck_DataTypeColumnValidation"
        >>> vd.results[key]["result"]["status"]
        'Success'
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    def __init__(
        self,
        column: str | None = None,
        column_type: type | None = None,
        frame_schema_definition: dict[str, type] | None = None,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
        **kwargs: KwargsParams,
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
        self.schema_length = schema.len()
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
