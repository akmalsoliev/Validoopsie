from datetime import date, datetime
from typing import Any, Literal, Union

from narwhals.typing import IntoFrame

from validoopsie.base.base_validation import BaseValidation

class Validate:
    """Main validation class that provides a fluent interface for applying validations.

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> from narwhals.dtypes import IntegerType
        >>> from validoopsie import Validate
        >>>
        >>> # Create a dataframe and apply multiple validations
        >>> df = pd.DataFrame({
        ...     "id": [1, 2, 3],
        ...     "name": ["Alice", "Bob", "Charlie"],
        ...     "age": [25, 30, 35],
        ...     "email": ["alice@example.com", "bob@example.com", "charlie@example.com"]
        ... })
        >>>
        >>> # Chain validations together
        >>> vd = (
        ...     Validate(df)
        ...     .TypeValidation.TypeCheck(column="id", column_type=IntegerType)
        ...     .ValuesValidation.ColumnValuesToBeBetween(column="age", min_value=18)
        ... )
        >>>
        >>> # All validations pass
        >>> list_of_validations = vd.results["Summary"]["validations"]
        >>> results = vd.results
        >>> all(results[v]["result"]["status"] == "Success" for v in list_of_validations)
        True
        >>>
        >>> # When calling validate on successful validation there is no error.
        >>> vd.validate()

    """

    frame: IntoFrame
    results: dict[str, Any]

    def __init__(self, frame: IntoFrame) -> None: ...
    def validate(self, *, raise_results: bool = False) -> Validate: ...
    def add_validation(self, validation: BaseValidation) -> Validate:
        """Add custom generated validation check to the Validate class instance.

        Args:
            validation (BaseValidationParameters): Custom validation check to add

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> from validoopsie import Validate
            >>> from validoopsie.base import BaseValidation
            >>>
            >>> # Create a custom validation class
            >>> class CustomValidation(BaseValidation):
            ...     def __init__(self, column, impact="low", threshold=0.0, **kwargs):
            ...         super().__init__(column, impact, threshold, **kwargs)
            ...
            ...     @property
            ...     def fail_message(self) -> str:
            ...         return f"Custom validation failed for column {self.column}"
            ...
            ...     def __call__(self, frame):
            ...         # Custom validation logic
            ...         return (
            ...             # Note: that select `None` for an empty DataFrame
            ...             frame.select(nw.all() == None)
            ...             .group_by(self.column)
            ...             .agg(nw.col("column1").sum().alias("column1-count"))
            ...         )
            ...
            >>> # Apply custom validation
            >>> df = pd.DataFrame({"column1": [1, 2, 3]})
            >>>
            >>> vd = (
            ...     Validate(df)
            ...     .add_validation(CustomValidation(column="column1"))
            ... )
            >>> key = "CustomValidation_column1"
            >>> vd.results[key]["result"]["status"]
            'Success'
            >>>
            >>> # When calling validate on successful validation there is no error.
            >>> vd.validate()

        """

    class DateValidation:
        @staticmethod
        def ColumnMatchDateFormat(
            column: str,
            date_format: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the values in a column match the date format.

            Implementation:
                :class:`validoopsie.validation_catalogue.DateValidation.column_match_date_format.ColumnMatchDateFormat`

            Args:
                column (str): Column to validate.
                date_format (str): Date format to check.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate dates match format
                >>> df = pd.DataFrame({
                ...     "dates_iso": ["2023-01-01", "2023-02-15", "2023-03-30"],
                ...     "dates_mixed": ["2023-01-01", "02/15/2023", "2023-03-30"]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .DateValidation.ColumnMatchDateFormat(
                ...         column="dates_iso",
                ...         date_format="YYYY-mm-dd"
                ...     )
                ... )
                >>> key = "ColumnMatchDateFormat_dates_iso"
                >>> vd.results[key]["result"]["status"]
                'Success'

                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()
                >>>
                >>> # With threshold allowing some failures
                >>> vd2 = (
                ...     Validate(df)
                ...     .DateValidation.ColumnMatchDateFormat(
                ...         column="dates_mixed",
                ...         date_format="YYYY-mm-dd",
                ...         threshold=0.4  # Allow 40% failure rate
                ...     )
                ... )
                >>> key2 = "ColumnMatchDateFormat_dates_mixed"
                >>> vd2.results[key2]["result"]["status"]
                'Success'

            """

        @staticmethod
        def DateToBeBetween(
            column: str,
            min_date: date | datetime | None = None,
            max_date: date | datetime | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the values in a column are between the specified dates.

            Implementation:
                :class:`validoopsie.validation_catalogue.DateValidation.date_to_be_between.DateToBeBetween`

            Args:
                column (str): Column to validate.
                min_date (date | datetime | None): Minimum date for a column entry length.
                max_date (date | datetime | None): Maximum date for a column entry length.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>> from datetime import datetime
                >>>
                >>> # Validate dates are within range
                >>> df = pd.DataFrame({
                ...     "order_date": [
                ...         datetime(2023, 1, 15),
                ...         datetime(2023, 2, 20),
                ...         datetime(2023, 3, 25)
                ...     ]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .DateValidation.DateToBeBetween(
                ...         column="order_date",
                ...         min_date=datetime(2023, 1, 1),
                ...         max_date=datetime(2023, 12, 31)
                ...     )
                ... )
                >>> key = "DateToBeBetween_order_date"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

    class EqualityValidation:
        @staticmethod
        def PairColumnEquality(
            column: str,
            target_column: str,
            group_by_combined: bool = True,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the pair of columns are equal.

            Implementation:
                :class:`validoopsie.validation_catalogue.EqualityValidation.pair_column_equality.PairColumnEquality`

            Args:
                column (str): Column to validate.
                target_column (str): Column to compare.
                group_by_combined (bool, optional): Group by combine columns.
                    Default True.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate columns match
                >>> df = pd.DataFrame({
                ...     "amount": [100, 200, 300],
                ...     "verified_amount": [100, 200, 300]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .EqualityValidation.PairColumnEquality(
                ...         column="amount",
                ...         target_column="verified_amount"
                ...     )
                ... )
                >>> key = "PairColumnEquality_amount"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

    class NullValidation:
        @staticmethod
        def ColumnBeNull(
            column: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the values in a column are null.

            Implementation:
                :class:`validoopsie.validation_catalogue.NullValidation.column_be_null.ColumnBeNull`

            Args:
                column (str): Column to validate.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate field contains only nulls
                >>> df = pd.DataFrame({
                ...     "id": [1, 2, 3],
                ...     "optional_field": [None, None, None]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .NullValidation.ColumnBeNull(column="optional_field")
                ... )
                >>> key = "ColumnBeNull_optional_field"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def ColumnNotBeNull(
            column: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the values in a column are not null.

            Implementation:
                :class:`validoopsie.validation_catalogue.NullValidation.column_not_be_null.ColumnNotBeNull`

            Args:
                column (str): Column to validate.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate field has no nulls
                >>> df = pd.DataFrame({
                ...     "id": [1, 2, 3],
                ...     "required_field": ["a", "b", "c"]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .NullValidation.ColumnNotBeNull(column="required_field")
                ... )
                >>> key = "ColumnNotBeNull_required_field"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

    class StringValidation:
        @staticmethod
        def LengthToBeBetween(
            column: str,
            min_value: int | None = None,
            max_value: int | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the string lengths are between the specified range.

            Implementation:
                :class:`validoopsie.validation_catalogue.StringValidation.length_to_be_between.LengthToBeBetween`

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

            Examples:
                >>> import pandas as pd
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Validate string length
                >>> df = pd.DataFrame({
                ...     "username": ["user1", "user2", "user3"],
                ...     "password": ["pass123", "password", "p@ssw0rd"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> vd = (
                ...     Validate(frame)
                ...     .StringValidation.LengthToBeBetween(
                ...         column="password",
                ...         min_value=6,
                ...         max_value=10
                ...     )
                ... )
                >>> key = "LengthToBeBetween_password"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def LengthToBeEqualTo(
            column: str,
            value: int,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Expect the column entries to be strings with length equal to `value`.

            Implementation:
                :class:`validoopsie.validation_catalogue.StringValidation.length_to_be_equal_to.LengthToBeEqualTo`

            Args:
                column (str): Column to validate.
                value (int): The expected value for a column entry length.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate text doesn't contain pattern
                >>> df = pd.DataFrame({
                ...     "comment": ["Great product!", "Normal comment", "Just okay"]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .StringValidation.NotPatternMatch(
                ...         column="comment",
                ...         pattern=r"password"
                ...     )
                ... )
                >>> key = "NotPatternMatch_comment"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def NotPatternMatch(
            column: str,
            pattern: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Expect the column entries to be strings that do not pattern match.

            Implementation:
                :class:`validoopsie.validation_catalogue.StringValidation.not_pattern_match.NotPatternMatch`

            Args:
                column (str): The column name.
                pattern (str): The pattern expression the column should not match.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate text doesn't contain pattern
                >>> df = pd.DataFrame({
                ...     "comment": ["Great product!", "Normal comment", "Just okay"]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .StringValidation.NotPatternMatch(
                ...         column="comment",
                ...         pattern=r"password"
                ...     )
                ... )
                >>> key = "NotPatternMatch_comment"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def PatternMatch(
            column: str,
            pattern: str,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            r"""Expect the column entries to be strings that pattern matches.

            Implementation:
                :class:`validoopsie.validation_catalogue.StringValidation.pattern_match.PatternMatch`

            Args:
                column (str): The column name.
                pattern (str): The pattern expression the column should match.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate email format
                >>> df = pd.DataFrame({
                ...     "email": ["user1@example.com", "user2@example.com"]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .StringValidation.PatternMatch(
                ...         column="email",
                ...         pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                ...     )
                ... )
                >>> key = "PatternMatch_email"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

    class TypeValidation:
        @staticmethod
        def TypeCheck(
            column: str | None = None,
            column_type: type | None = None,
            frame_schema_definition: dict[str, type] | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Validate the data type of the column(s).

            Implementation:
                :class:`validoopsie.validation_catalogue.TypeValidation.type_check.TypeCheck`

            Args:
                column (str | None): The column to validate.
                column_type (type | None): The type of validation to perform.
                frame_schema_definition (dict[str, type] | None): A dictionary
                    of column names and their respective validation types.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

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

    class UniqueValidation:
        @staticmethod
        def ColumnUniquePair(
            column_list: list[str] | tuple[str],
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Validates the uniqueness of combined values from multiple columns.

            Implementation:
                :class:`validoopsie.validation_catalogue.UniqueValidation.column_unique_pair.ColumnUniquePair`

            This class checks if the combination of values from specified columns creates
            unique entries in the dataset. For example, if checking columns ['first_name',
            'last_name'], the combination of these values should be unique for each row.

            Args:
                column_list (list | tuple): List or tuple of column names to check for
                    unique combinations.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate unique pairs
                >>> df = pd.DataFrame({
                ...     "student_id": [101, 102, 103],
                ...     "course_id": [201, 202, 203],
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .UniqueValidation.ColumnUniquePair(
                ...         column_list=["student_id", "course_id"]
                ...     )
                ... )
                >>> key = "ColumnUniquePair_student_id - course_id"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def ColumnUniqueValueCountToBeBetween(
            column: str,
            min_value: int | None = None,
            max_value: int | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check the number of unique values in a column to be between min and max.

            Implementation:
                :class:`validoopsie.validation_catalogue.UniqueValidation.column_unique_value_count_to_be_between.ColumnUniqueValueCountToBeBetween`

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

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate number of unique values
                >>> df = pd.DataFrame({
                ...     "category": ["A", "B", "C", "A", "B"]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .UniqueValidation.ColumnUniqueValueCountToBeBetween(
                ...         column="category",
                ...         min_value=1,
                ...         max_value=5
                ...     )
                ... )
                >>> key = "ColumnUniqueValueCountToBeBetween_category"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def ColumnUniqueValuesToBeInList(
            column: str,
            values: list[Union[str, float, int, None]],
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the unique values are in the list.

            Implementation:
                :class:`validoopsie.validation_catalogue.UniqueValidation.column_unique_values_to_be_in_list.ColumnUniqueValuesToBeInList`

            Args:
                column (str): Column to validate.
                values (list[Union[str, float, int, None]]): List of values to check.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate values in allowed list
                >>> df = pd.DataFrame({
                ...     "status": ["active", "inactive", "pending"]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .UniqueValidation.ColumnUniqueValuesToBeInList(
                ...         column="status",
                ...         values=["active", "inactive", "pending"]
                ...     )
                ... )
                >>> key = "ColumnUniqueValuesToBeInList_status"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

    class ValuesValidation:
        @staticmethod
        def ColumnValuesToBeBetween(
            column: str,
            min_value: float | None = None,
            max_value: float | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the values in a column are between a range.

            Implementation:
                :class:`validoopsie.validation_catalogue.ValuesValidation.column_values_to_be_between.ColumnValuesToBeBetween`

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

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate numeric range
                >>> df = pd.DataFrame({
                ...     "age": [25, 30, 42, 18, 65]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .ValuesValidation.ColumnValuesToBeBetween(
                ...         column="age",
                ...         min_value=18,
                ...         max_value=65
                ...     )
                ... )
                >>> key = "ColumnValuesToBeBetween_age"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def ColumnsSumToBeBetween(
            columns_list: list[str],
            min_sum_value: float | None = None,
            max_sum_value: float | None = None,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the sum of columns is between min and max values.

            Implementation:
                :class:`validoopsie.validation_catalogue.ValuesValidation.columns_sum_to_be_between.ColumnsSumToBeBetween`

            If the `min_value` or `max_value` is not provided then other will be used as
            the threshold.

            If neither `min_value` nor `max_value` is provided, then the validation will
            result in failure.

            Args:
                columns_list (list[str]): List of columns to sum.
                min_sum_value (float | None): Minimum sum value that columns should be
                    greater than or equal to.
                max_sum_value (float | None): Maximum sum value that columns should be
                    less than or equal to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate macronutrient sum in range
                >>> df = pd.DataFrame({
                ...     "protein": [26],
                ...     "fat": [19],
                ...     "carbs": [0]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .ValuesValidation.ColumnsSumToBeBetween(
                ...         columns_list=["protein", "fat", "carbs"],
                ...         min_sum_value=30,
                ...         max_sum_value=50
                ...     )
                ... )
                >>> key = "ColumnsSumToBeBetween_protein-fat-carbs-combined"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """

        @staticmethod
        def ColumnsSumToBeEqualTo(
            columns_list: list[str],
            sum_value: float,
            threshold: float = 0.00,
            impact: Literal["low", "medium", "high"] = "low",
        ) -> Validate:
            """Check if the sum of the columns is equal to a specific value.

            Implementation:
                :class:`validoopsie.validation_catalogue.ValuesValidation.columns_sum_to_be_equal_to.ColumnsSumToBeEqualTo`

            Args:
                columns_list (list[str]): List of columns to sum.
                sum_value (float): Value that the columns should sum to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> from validoopsie import Validate
                >>>
                >>> # Validate component sum equals total
                >>> df = pd.DataFrame({
                ...     "hardware": [5000],
                ...     "software": [3000],
                ...     "personnel": [12000],
                ...     "total": [20000]
                ... })
                >>>
                >>> vd = (
                ...     Validate(df)
                ...     .ValuesValidation.ColumnsSumToBeEqualTo(
                ...         columns_list=["hardware", "software", "personnel"],
                ...         sum_value=20000
                ...     )
                ... )
                >>> key = "ColumnsSumToBeEqualTo_hardware-software-personnel-combined"
                >>> vd.results[key]["result"]["status"]
                'Success'
                >>>
                >>> # When calling validate on successful validation there is no error.
                >>> vd.validate()

            """
