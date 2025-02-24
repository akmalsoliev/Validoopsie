from datetime import date, datetime
from typing import Any, Literal, Union

from narwhals.typing import IntoFrame

from validoopsie.base.base_validation_parameters import BaseValidationParameters
from validoopsie.typing import KwargsType

class Validate:
    frame: IntoFrame
    results: dict[str, Any]

    def __init__(self, frame: IntoFrame) -> None: ...
    def validate(self, raise_results: bool = False) -> Validate: ...
    def add_validation(self, validation: BaseValidationParameters) -> Validate:
        """Add custom generated validation check to the Validate class instance.

        Args:
            validation (type): Custom generated validation check

        """

    class DateValidation:
        @staticmethod
        def ColumnMatchDateFormat(
            column: str,
            date_format: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column match the date format.

            Args:
                column (str): Column to validate.
                date_format (str): Date format to check.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def DateToBeBetween(
            column: str,
            min_date: date | datetime | None = None,
            max_date: date | datetime | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are between the specified dates.

            Args:
                column (str): Column to validate.
                min_date (date | datetime | None): Minimum date for a column entry length.
                max_date (date | datetime | None): Maximum date for a column entry length.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

    class EqualityValidation:
        @staticmethod
        def PairColumnEquality(
            column: str,
            target_column: str,
            group_by_combined: bool = True,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the pair of columns are equal.

            Args:
                column (str): Column to validate.
                target_column (str): Column to compare.
                group_by_combined (bool, optional): Group by combine columns.
                    Default True.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

    class NullValidation:
        @staticmethod
        def ColumnBeNull(
            column: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are null.

            Args:
                column (str): Column to validate.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnNotBeNull(
            column: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are not null.

            Args:
                column (str): Column to validate.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

    class StringValidation:
        @staticmethod
        def LengthToBeBetween(
            column: str,
            min_value: int | None = None,
            max_value: int | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the string lengths are between the specified range.

            If the `min_value` or `max_value` is not provided then other will be used as
            the threshold.

            If neither `min_value` nor `max_value` is provided, then the validation will
            result in failure.

            Args:
                column (str): Column to validate.
                min_value (float | None): Minimum value for a column entry length.
                max_value (float | None): Maximum value for a column entry length.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def LengthToBeEqualTo(
            column: str,
            value: int,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Expect the column entries to be strings with length equal to `value`.

            Args:
                column (str): Column to validate.
                value (int): The expected value for a column entry length.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def NotPatternMatch(
            column: str,
            pattern: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Expect the column entries to be strings that do not pattern match.

            Args:
                column (str): The column name.
                pattern (str): The pattern expression the column should not match.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def PatternMatch(
            column: str,
            pattern: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Expect the column entries to be strings that pattern matches.

            Args:
                column (str): The column name.
                pattern (str): The pattern expression the column should match.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

    class TypeValidation:
        @staticmethod
        def TypeCheck(
            column: str | None = None,
            column_type: type | None = None,
            frame_schema_definition: dict[str, type] | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Validate the data type of the column(s).

            Parameters:
                column (str | None): The column to validate.
                column_type (type | None): The type of validation to perform.
                frame_schema_definition (dict[str, ValidoopsieType] | None): A dictionary
                    of column names and their respective validation types.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.


            ```python
            import narwhals
            from narwhals.dtypes import (
                IntegerType,
                FloatType,
                StringType,
            )
            import pandas as pd
            from validoopsie import Validate


            df = pd.DataFrame({
                "IntType": [1, -15],
                "FloatType": [1.23, -45.67],
                "String": ["hello", "world"],
            })

            vd = Validate(df)
            vd.TypeValidation.TypeCheck(
                column="IntType",
                column_type=IntegerType,
            )

            # or you can always use the dictionary
            column_type_definitions = {
                "IntType": IntegerType,
                "FloatType": FloatType,
                "String": StringType,
            }
            vd.TypeValidation.TypeCheck(
                frame_schema_definition=column_type_definitions,
            )

            ```

            """

    class UniqueValidation:
        @staticmethod
        def ColumnUniquePair(
            column_list: list | tuple,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Validates the uniqueness of combined values from multiple columns.

            This class checks if the combination of values from specified columns creates
            unique entries in the dataset. For example, if checking columns ['first_name',
            'last_name'], the combination of these values should be unique for each row.

            Parameters
              column_list (list | tuple): List or tuple of column names to check for
                  unique combinations.
              threshold (float, optional): Threshold for validation. Defaults to 0.0.
              impact (Literal["low", "medium", "high"], optional): Impact level of
                  validation. Defaults to "low".

            """

        @staticmethod
        def ColumnUniqueValueCountToBeBetween(
            column: str,
            min_value: int | None = None,
            max_value: int | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check the number of unique values in a column to be between min and max.

            If the `min_value` or `max_value` is not provided then other will be used as
            the threshold.

            If neither `min_value` nor `max_value` is provided, then the validation will
            result in failure.

            Args:
                column (str): The column to validate.
                min_value (int or None): The minimum number of unique values allowed.
                max_value (int or None): The maximum number of unique values allowed.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnUniqueValuesToBeInList(
            column: str,
            values: list[Union[str, float, int, None]],
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the unique values are in the list.

            Args:
                column (str): Column to validate.
                values (list[Union[str, float, int, None]]): List of values to check.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

    class ValuesValidation:
        @staticmethod
        def ColumnValuesToBeBetween(
            column: str,
            min_value: float | None = None,
            max_value: float | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are between a range.

            If the `min_value` or `max_value` is not provided then other will be used as
            the threshold.

            If neither `min_value` nor `max_value` is provided, then the validation will
            result in failure.


            Args:
                column (str): Column to validate.
                min_value (float | None): Minimum value for a column entry length.
                max_value (float | None): Maximum value for a column entry length.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnsSumToBeEqualTo(
            columns_list: list[str],
            sum_value: float,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the sum of the columns is equal to a specific value.

            Args:
                columns_list (list[str]): List of columns to sum.
                sum_value (float): Value that the columns should sum to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnsSumToBeBetween(
            columns_list: list[str],
            min_sum_value: float | None = None,
            max_sum_value: float | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the sum of columns is greater than or equal to `max_sum`.

            If the `min_value` or `max_value` is not provided then other will be used as
            the threshold.

            If neither `min_value` nor `max_value` is provided, then the validation will
            result in failure.

            Args:
                columns_list (list[str]): List of columns to sum.
                max_sum_value (float | None): Minimum sum value that columns should be
                    greater than or equal to.
                min_sum_value (float | None): Maximum sum value that columns should be
                    less than or equal to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".
                kwargs: KwargsType (dict): Additional keyword arguments.

            """
