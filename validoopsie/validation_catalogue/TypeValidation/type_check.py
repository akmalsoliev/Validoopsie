from __future__ import annotations

import narwhals as nw
from narwhals.dtypes import DType
from narwhals.typing import Frame

from validoopsie.base import BaseValidationParameters, base_validation_wrapper


@base_validation_wrapper
class TypeCheck(BaseValidationParameters):
    """Validate the data type of the column(s).

    If the column and `validation_type` is not provided then `column_type_definitions`
    dictionary should be required to validate multiple columns.

    Operator can use the generic column data type provided by Validoopsie
    (e.g. `IntegerType`) or more specific type provided by Narwhals
    (e.g. `narwhals.Int64`).

    For a full list of types refer to:

    * [Validoopsie Generic Types](https://akmalsoliev.github.io/Validoopsie/typing.html#typing.FloatType)
    * [Narwhals Specific Types](https://narwhals-dev.github.io/narwhals/api-reference/dtypes/)

    Example of the `column_type_definitions`:

    ```python

    from validoopsie.types import IntegerType
    import narwhals

    {
        "column1": IntegerType,
        "column2": narwhals.Int64,
    }
    ```

    Parameters:
        column (str | None): The column to validate.
        column_type (type | None): The type of validation to perform.
        frame_schema_definition (dict[str, ValidoopsieType] | None): A dictionary of
            column names and their respective validation types.
        threshold (float, optional): Threshold for validation. Defaults to 0.0.
        impact (Literal["low", "medium", "high"], optional): Impact level of validation.
            Defaults to "low".
        kwargs: KwargsType (dict): Additional keyword arguments.

    """

    def __init__(
        self,
        column: str | None = None,
        column_type: type | None = None,
        frame_schema_definition: dict[str, type] | None = None,
        *args,
        **kwargs,
    ) -> None:
        # Single validation check
        if column and column_type:
            self.__check_validation_parameter__(column, column_type, DType)
            self.column_type = column_type
            self.frame_schema_definition = {column: column_type}

        # Multiple validation checks
        elif not column and not column_type and frame_schema_definition:
            # Check if Validation inside of the dictionary is actually correct
            [
                self.__check_validation_parameter__(column, vtype, DType)
                for column, vtype in frame_schema_definition.items()
            ]

            column = "DataTypeColumnValidation"
            self.frame_schema_definition = frame_schema_definition
        else:
            error_message = (
                "Either `column` and `validation_type` should be provided or "
                "`frame_schema_definition` should be provided.",
            )
            raise ValueError(error_message)

        super().__init__(column, *args, **kwargs)

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

            if not issubclass(defined_type, column_type.__class__):
                failed_columns.append(column_name)

        native_namespace = nw.get_native_namespace(frame)
        return nw.from_dict(
            {self.column: failed_columns},
            native_namespace=native_namespace,
        ).with_columns(
            nw.lit(1).alias(f"{self.column}-count"),
        )
