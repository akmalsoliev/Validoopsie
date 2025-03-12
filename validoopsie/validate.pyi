from datetime import date, datetime
from typing import Any, Literal, Union

from narwhals.typing import IntoFrame

from validoopsie.base.base_validation import BaseValidation

class Validate:
    r"""Main validation class that provides a fluent interface for applying validations.

    Examples:
        >>> import pandas as pd
        >>> import narwhals as nw
        >>> from validoopsie import Validate
        >>>
        >>> # Create a simple dataframe for testing
        >>> df = pd.DataFrame({
        ...     "id": [1, 2, 3, 4, 5],
        ...     "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        ...     "age": [25, 30, 35, 40, 45],
        ...     "email": [
        ...         "alice@example.com", "bob@example.com", "charlie@example.com",
        ...         "david@example.com", "eve@example.com"
        ...     ]
        ... })
        >>> frame = nw.from_native(df)
        >>>
        >>> # Create a Validate instance and apply multiple validations
        >>> vd = Validate(frame)
        >>> vd.TypeValidation.TypeCheck(
        ...     column="id",
        ...     column_type=int
        ... ).StringValidation.PatternMatch(
        ...     column="email",
        ...     pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ... ).ValuesValidation.ColumnValuesToBeBetween(
        ...     column="age",
        ...     min_value=18,
        ...     max_value=100
        ... )
        >>>
        >>> # Execute validations
        >>> result = vd.validate()
        >>>
        >>> # All validations should pass
        >>> assert all(v["result"]["status"] == "Success"
        ...            for v in vd.results.values())
        >>>
        >>> # With a failing validation
        >>> df_with_error = pd.DataFrame({
        ...     "id": [1, 2, 3, 4, 5],
        ...     "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        ...     "age": [25, 30, 15, 40, 45],  # Age 15 is below our min_value of 18
        ...     "email": [
        ...         "alice@example.com", "bob@example.com", "charlie@example.com",
        ...         "david@example.com", "eve@example.com"
        ...     ]
        ... })
        >>> frame_with_error = nw.from_native(df_with_error)
        >>>
        >>> vd_with_error = Validate(frame_with_error)
        >>> vd_with_error.ValuesValidation.ColumnValuesToBeBetween(
        ...     column="age",
        ...     min_value=18,
        ...     max_value=100,
        ...     impact="high"
        ... )
        >>>
        >>> # This should raise a ValueError due to the failing validation
        >>> # with high impact
        >>> try:
        ...     vd_with_error.validate(raise_results=True)
        ... except ValueError:
        ...     print("Validation failed as expected")
        Validation failed as expected
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
            ...         # Custom validation logic here
            ...         # For this example, just return an empty frame (validation passes)
            ...         return frame.filter(False)
            ...
            >>> # Create a simple dataframe
            >>> df = pd.DataFrame({"column1": [1, 2, 3]})
            >>> frame = nw.from_native(df)
            >>>
            >>> # Create a Validate instance and add custom validation
            >>> vd = Validate(frame)
            >>> custom_validation = CustomValidation(column="column1")
            >>> vd.add_validation(custom_validation)
            >>>
            >>> # Execute validation
            >>> vd.validate()
            >>>
            >>> # Validation should pass
            >>> assert vd.results["CustomValidation_column1"]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with date columns
                >>> df = pd.DataFrame({
                ...     "dates_iso": ["2023-01-01", "2023-02-15", "2023-03-30"],
                ...     "dates_us": ["01/01/2023", "02/15/2023", "03/30/2023"],
                ...     "dates_mixed": ["2023-01-01", "02/15/2023", "2023-03-30"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Create a Validate instance with multiple date format validations
                >>> vd = Validate(frame)
                >>> vd.DateValidation.ColumnMatchDateFormat(
                ...     column="dates_iso",
                ...     date_format="YYYY-mm-dd"
                ... ).DateValidation.ColumnMatchDateFormat(
                ...     column="dates_us",
                ...     date_format="mm/dd/YYYY"
                ... )
                >>>
                >>> # Execute validations
                >>> vd.validate()
                >>>
                >>> # Both validations should pass
                >>> assert vd.results["ColumnMatchDateFormat_dates_iso"]["result"]["status"] == "Success"
                >>> assert vd.results["ColumnMatchDateFormat_dates_us"]["result"]["status"] == "Success"
                >>>
                >>> # Mixed format column will fail
                >>> vd_mixed = Validate(frame)
                >>> vd_mixed.DateValidation.ColumnMatchDateFormat(
                ...     column="dates_mixed",
                ...     date_format="YYYY-mm-dd"
                ... )
                >>> vd_mixed.validate()
                >>> assert vd_mixed.results["ColumnMatchDateFormat_dates_mixed"]["result"]["status"] == "Fail"
                >>>
                >>> # But it can pass with a threshold
                >>> vd_threshold = Validate(frame)
                >>> vd_threshold.DateValidation.ColumnMatchDateFormat(
                ...     column="dates_mixed",
                ...     date_format="YYYY-mm-dd",
                ...     threshold=0.4  # Allow 40% failure rate
                ... )
                >>> vd_threshold.validate()
                >>> assert vd_threshold.results["ColumnMatchDateFormat_dates_mixed"]["result"]["status"] == "Success"
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
                >>> # Create test dataframe with dates
                >>> df = pd.DataFrame({
                ...     "order_date": [
                ...         "2023-01-15", "2023-02-20", "2023-03-25",
                ...         "2023-04-30", "2023-05-05"
                ...     ]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate that dates are within a specific range
                >>> vd = Validate(frame)
                >>> vd.DateValidation.DateToBeBetween(
                ...     column="order_date",
                ...     min_date=datetime(2023, 1, 1),
                ...     max_date=datetime(2023, 12, 31)
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Validation should pass
                >>> assert vd.results["DateToBeBetween_order_date"]["result"]["status"] == "Success"
                >>>
                >>> # Test with dates outside the range
                >>> df_invalid = pd.DataFrame({
                ...     "order_date": [
                ...         "2023-01-15", "2023-02-20", "2022-12-25",  # This date is too early
                ...         "2023-04-30", "2024-01-05"  # This date is too late
                ...     ]
                ... })
                >>> frame_invalid = nw.from_native(df_invalid)
                >>>
                >>> # Validate with same constraints
                >>> vd_invalid = Validate(frame_invalid)
                >>> vd_invalid.DateValidation.DateToBeBetween(
                ...     column="order_date",
                ...     min_date=datetime(2023, 1, 1),
                ...     max_date=datetime(2023, 12, 31)
                ... )
                >>>
                >>> # Execute validation
                >>> vd_invalid.validate()
                >>>
                >>> # Should fail with dates outside range
                >>> assert vd_invalid.results["DateToBeBetween_order_date"]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some failures
                >>> vd_threshold = Validate(frame_invalid)
                >>> vd_threshold.DateValidation.DateToBeBetween(
                ...     column="order_date",
                ...     min_date=datetime(2023, 1, 1),
                ...     max_date=datetime(2023, 12, 31),
                ...     threshold=0.4  # Allow 40% failure rate
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results["DateToBeBetween_order_date"]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with matching columns
                >>> df = pd.DataFrame({
                ...     "amount": [100, 200, 300, 400, 500],
                ...     "verified_amount": [100, 200, 300, 400, 500],
                ...     "customer_id": [1, 2, 3, 4, 5],
                ...     "profile_id": [1, 2, 3, 4, 5]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate that pairs of columns match
                >>> vd = Validate(frame)
                >>> vd.EqualityValidation.PairColumnEquality(
                ...     column="amount",
                ...     target_column="verified_amount"
                ... ).EqualityValidation.PairColumnEquality(
                ...     column="customer_id",
                ...     target_column="profile_id"
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Both validations should pass
                >>> amount_key = "PairColumnEquality_amount_verified_amount"
                >>> id_key = "PairColumnEquality_customer_id_profile_id"
                >>> assert vd.results[amount_key]["result"]["status"] == "Success"
                >>> assert vd.results[id_key]["result"]["status"] == "Success"
                >>>
                >>> # With mismatched data
                >>> df_mismatch = pd.DataFrame({
                ...     "amount": [100, 200, 300, 400, 500],
                ...     "verified_amount": [100, 200, 350, 400, 500],  # Mismatch in value
                ...     "customer_id": [1, 2, 3, 4, 5],
                ...     "profile_id": [1, 2, 3, 4, 6]  # Mismatch in value
                ... })
                >>> frame_mismatch = nw.from_native(df_mismatch)
                >>>
                >>> # Apply same validations
                >>> vd_mismatch = Validate(frame_mismatch)
                >>> vd_mismatch.EqualityValidation.PairColumnEquality(
                ...     column="amount",
                ...     target_column="verified_amount"
                ... ).EqualityValidation.PairColumnEquality(
                ...     column="customer_id",
                ...     target_column="profile_id"
                ... )
                >>>
                >>> # Execute validation
                >>> vd_mismatch.validate()
                >>>
                >>> # Both validations should fail
                >>> assert vd_mismatch.results[amount_key]["result"]["status"] == "Fail"
                >>> assert vd_mismatch.results[id_key]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some failures
                >>> vd_threshold = Validate(frame_mismatch)
                >>> vd_threshold.EqualityValidation.PairColumnEquality(
                ...     column="amount",
                ...     target_column="verified_amount",
                ...     threshold=0.2  # Allow 20% failure rate
                ... ).EqualityValidation.PairColumnEquality(
                ...     column="customer_id",
                ...     target_column="profile_id",
                ...     threshold=0.2  # Allow 20% failure rate
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results[amount_key]["result"]["status"] == "Success"
                >>> assert vd_threshold.results[id_key]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>> import numpy as np
                >>>
                >>> # Create test dataframe with null values
                >>> df = pd.DataFrame({
                ...     "id": [1, 2, 3, 4, 5],
                ...     "required_field": ["a", "b", "c", "d", "e"],
                ...     "optional_field": [None, None, None, None, None]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate that optional field contains only nulls
                >>> vd = Validate(frame)
                >>> vd.NullValidation.ColumnBeNull(
                ...     column="optional_field"
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Validation should pass
                >>> assert vd.results["ColumnBeNull_optional_field"]["result"]["status"] == "Success"
                >>>
                >>> # With mixed null/non-null values
                >>> df_mixed = pd.DataFrame({
                ...     "id": [1, 2, 3, 4, 5],
                ...     "required_field": ["a", "b", "c", "d", "e"],
                ...     "optional_field": [None, "value", None, None, "another"]
                ... })
                >>> frame_mixed = nw.from_native(df_mixed)
                >>>
                >>> # Apply same validation
                >>> vd_mixed = Validate(frame_mixed)
                >>> vd_mixed.NullValidation.ColumnBeNull(
                ...     column="optional_field"
                ... )
                >>>
                >>> # Execute validation
                >>> vd_mixed.validate()
                >>>
                >>> # Should fail with non-null values
                >>> assert vd_mixed.results["ColumnBeNull_optional_field"]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some non-null values
                >>> vd_threshold = Validate(frame_mixed)
                >>> vd_threshold.NullValidation.ColumnBeNull(
                ...     column="optional_field",
                ...     threshold=0.4  # Allow 40% non-null values
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results["ColumnBeNull_optional_field"]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>> import numpy as np
                >>>
                >>> # Create test dataframe with non-null and null values
                >>> df = pd.DataFrame({
                ...     "id": [1, 2, 3, 4, 5],
                ...     "required_field": ["a", "b", "c", "d", "e"],
                ...     "optional_field": [None, "value", None, None, "another"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate that required field has no nulls
                >>> vd = Validate(frame)
                >>> vd.NullValidation.ColumnNotBeNull(
                ...     column="required_field"
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Validation should pass
                >>> assert vd.results["ColumnNotBeNull_required_field"]["result"]["status"] == "Success"
                >>>
                >>> # Test with optional field that has nulls
                >>> vd_optional = Validate(frame)
                >>> vd_optional.NullValidation.ColumnNotBeNull(
                ...     column="optional_field"
                ... )
                >>>
                >>> # Execute validation
                >>> vd_optional.validate()
                >>>
                >>> # Should fail with null values
                >>> assert vd_optional.results["ColumnNotBeNull_optional_field"]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some null values
                >>> vd_threshold = Validate(frame)
                >>> vd_threshold.NullValidation.ColumnNotBeNull(
                ...     column="optional_field",
                ...     threshold=0.6  # Allow 60% null values
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results["ColumnNotBeNull_optional_field"]["result"]["status"] == "Success"
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
                >>> # Create test dataframe with string data
                >>> df = pd.DataFrame({
                ...     "username": ["user1", "user2", "user3", "user4", "user5"],
                ...     "password": ["pass123", "password", "p@ssw0rd", "secret", "12345"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate password length is between 6 and 10 characters
                >>> vd = Validate(frame)
                >>> vd.StringValidation.LengthToBeBetween(
                ...     column="password",
                ...     min_value=6,
                ...     max_value=10
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should fail with some passwords outside range
                >>> assert vd.results["LengthToBeBetween_password"]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some failures
                >>> vd_threshold = Validate(frame)
                >>> vd_threshold.StringValidation.LengthToBeBetween(
                ...     column="password",
                ...     min_value=6,
                ...     max_value=10,
                ...     threshold=0.4  # Allow 40% failures
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results["LengthToBeBetween_password"]["result"]["status"] == "Success"
                >>>
                >>> # Test with only min_value constraint
                >>> vd_min = Validate(frame)
                >>> vd_min.StringValidation.LengthToBeBetween(
                ...     column="password",
                ...     min_value=5
                ... )
                >>>
                >>> # Execute validation
                >>> vd_min.validate()
                >>>
                >>> # Should pass as all passwords are at least 5 chars
                >>> assert vd_min.results["LengthToBeBetween_password"]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with fixed-length codes
                >>> df = pd.DataFrame({
                ...     "product_code": ["ABC123", "DEF456", "GHI789", "JKL012", "XYZ987"],
                ...     "country_code": ["US", "UK", "FR", "DE", "JP"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate country codes are exactly 2 characters
                >>> vd = Validate(frame)
                >>> vd.StringValidation.LengthToBeEqualTo(
                ...     column="country_code",
                ...     value=2
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Validation should pass
                >>> assert vd.results["LengthToBeEqualTo_country_code"]["result"]["status"] == "Success"
                >>>
                >>> # Validate product codes are exactly 6 characters
                >>> vd_product = Validate(frame)
                >>> vd_product.StringValidation.LengthToBeEqualTo(
                ...     column="product_code",
                ...     value=6
                ... )
                >>>
                >>> # Execute validation
                >>> vd_product.validate()
                >>>
                >>> # Validation should pass
                >>> assert vd_product.results["LengthToBeEqualTo_product_code"]["result"]["status"] == "Success"
                >>>
                >>> # Test with varying length codes
                >>> df_varying = pd.DataFrame({
                ...     "product_code": ["ABC123", "DEF456", "GHI789", "JK12", "XYZ9876"],
                ...     "country_code": ["US", "UK", "FRA", "DE", "JP"]
                ... })
                >>> frame_varying = nw.from_native(df_varying)
                >>>
                >>> # Apply same validations
                >>> vd_varying = Validate(frame_varying)
                >>> vd_varying.StringValidation.LengthToBeEqualTo(
                ...     column="product_code",
                ...     value=6
                ... ).StringValidation.LengthToBeEqualTo(
                ...     column="country_code",
                ...     value=2
                ... )
                >>>
                >>> # Execute validation
                >>> vd_varying.validate()
                >>>
                >>> # Both validations should fail
                >>> assert vd_varying.results["LengthToBeEqualTo_product_code"]["result"]["status"] == "Fail"
                >>> assert vd_varying.results["LengthToBeEqualTo_country_code"]["result"]["status"] == "Fail"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with text content
                >>> df = pd.DataFrame({
                ...     "username": ["john_doe", "jane_smith", "admin", "superuser", "guest"],
                ...     "comment": [
                ...         "Great product!",
                ...         "I had some issues with delivery",
                ...         "Contains sensitive information: password123",
                ...         "Normal comment",
                ...         "Another comment with password: xyz789"
                ...     ]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate comments don't contain the word 'password'
                >>> vd = Validate(frame)
                >>> vd.StringValidation.NotPatternMatch(
                ...     column="comment",
                ...     pattern=r"password"
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should fail with some comments containing 'password'
                >>> assert vd.results["NotPatternMatch_comment"]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some matches
                >>> vd_threshold = Validate(frame)
                >>> vd_threshold.StringValidation.NotPatternMatch(
                ...     column="comment",
                ...     pattern=r"password",
                ...     threshold=0.4  # Allow 40% containing 'password'
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results["NotPatternMatch_comment"]["result"]["status"] == "Success"
                >>>
                >>> # Validate usernames don't contain 'admin'
                >>> vd_admin = Validate(frame)
                >>> vd_admin.StringValidation.NotPatternMatch(
                ...     column="username",
                ...     pattern=r"admin"
                ... )
                >>>
                >>> # Execute validation
                >>> vd_admin.validate()
                >>>
                >>> # Should fail with username containing 'admin'
                >>> assert vd_admin.results["NotPatternMatch_username"]["result"]["status"] == "Fail"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with various formats
                >>> df = pd.DataFrame({
                ...     "email": [
                ...         "user1@example.com",
                ...         "user2@example.com",
                ...         "invalid-email",
                ...         "user4@example.com",
                ...         "user5@example"
                ...     ],
                ...     "phone": [
                ...         "123-456-7890",
                ...         "234-567-8901",
                ...         "345-678-9012",
                ...         "4567890123",
                ...         "567-89-0123"
                ...     ]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate email addresses match pattern
                >>> vd = Validate(frame)
                >>> vd.StringValidation.PatternMatch(
                ...     column="email",
                ...     pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should fail with some invalid emails
                >>> assert vd.results["PatternMatch_email"]["result"]["status"] == "Fail"
                >>>
                >>> # Validate phone numbers match pattern
                >>> vd_phone = Validate(frame)
                >>> vd_phone.StringValidation.PatternMatch(
                ...     column="phone",
                ...     pattern=r"^\d{3}-\d{3}-\d{4}$"
                ... )
                >>>
                >>> # Execute validation
                >>> vd_phone.validate()
                >>>
                >>> # Should fail with some invalid phone formats
                >>> assert vd_phone.results["PatternMatch_phone"]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some invalid formats
                >>> vd_threshold = Validate(frame)
                >>> vd_threshold.StringValidation.PatternMatch(
                ...     column="email",
                ...     pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                ...     threshold=0.4  # Allow 40% invalid emails
                ... ).StringValidation.PatternMatch(
                ...     column="phone",
                ...     pattern=r"^\d{3}-\d{3}-\d{4}$",
                ...     threshold=0.4  # Allow 40% invalid phones
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Both should pass with threshold
                >>> assert vd_threshold.results["PatternMatch_email"]["result"]["status"] == "Success"
                >>> assert vd_threshold.results["PatternMatch_phone"]["result"]["status"] == "Success"
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
            r"""Validate the data type of the column(s).

            Implementation:
                :class:`validoopsie.validation_catalogue.TypeValidation.type_check.TypeCheck`

            Parameters:
                column (str | None): The column to validate.
                column_type (type | None): The type of validation to perform.
                frame_schema_definition (dict[str, ValidoopsieType] | None): A dictionary
                    of column names and their respective validation types.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>> from narwhals.dtypes import IntegerType, FloatType, StringType
                >>>
                >>> # Create a dataframe for user profile validation
                >>> df = pd.DataFrame({
                ...     "user_id": [1001, 1002, 1003, 1004, 1005],
                ...     "username": ["user1", "user2", "user3", "user4", "user5"],
                ...     "email": [
                ...         "user1@example.com", "user2@example.com", "user3@example.com",
                ...         "user4@example.com", "user5@example.com"
                ...     ],
                ...     "age": [25, 30, 22, 41, 35],
                ...     "account_balance": [100.50, 250.75, 0.00, 1000.25, 50.00],
                ...     "is_active": [True, True, False, True, True]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Create a comprehensive validation
                >>> vd = Validate(frame)
                >>> vd.TypeValidation.TypeCheck(
                ...     frame_schema_definition={
                ...         "user_id": IntegerType,
                ...         "username": StringType,
                ...         "email": StringType,
                ...         "age": IntegerType,
                ...         "account_balance": FloatType
                ...     }
                ... ).StringValidation.PatternMatch(
                ...     column="email",
                ...     pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                ... ).ValuesValidation.ColumnValuesToBeBetween(
                ...     column="age",
                ...     min_value=18,
                ...     max_value=120
                ... ).StringValidation.LengthToBeBetween(
                ...     column="username",
                ...     min_value=3,
                ...     max_value=20
                ... )
                >>>
                >>> # Execute all validations
                >>> vd.validate()
                >>>
                >>> # Check results
                >>> type_check_key = next(k for k in vd.results.keys()
                ...                      if k.startswith("TypeCheck"))
                >>> assert vd.results[type_check_key]["result"]["status"] == "Success"
                >>> assert vd.results["PatternMatch_email"]["result"]["status"] == "Success"
                >>> assert vd.results["ColumnValuesToBeBetween_age"]["result"]["status"] == "Success"
                >>> assert vd.results["LengthToBeBetween_username"]["result"]["status"] == "Success"
                >>>
                >>> # Now with a dataframe containing invalid data
                >>> df_invalid = pd.DataFrame({
                ...     "user_id": [1001, 1002, 1003, 1004, 1005],
                ...     "username": ["u1", "user2", "user3", "user4", "user5"],  # Too short
                ...     "email": [
                ...         "user1@example.com", "invalid-email", "user3@example.com",
                ...         "user4@example.com", "user5@example.com"
                ...     ],  # Invalid email
                ...     "age": [25, 30, 15, 41, 35],  # Age below minimum
                ...     "account_balance": [100.50, 250.75, 0.00, 1000.25, 50.00],
                ...     "is_active": [True, True, False, True, True]
                ... })
                >>> frame_invalid = nw.from_native(df_invalid)
                >>>
                >>> # Apply same validations with high impact
                >>> vd_invalid = Validate(frame_invalid)
                >>> vd_invalid.TypeValidation.TypeCheck(
                ...     frame_schema_definition={
                ...         "user_id": IntegerType,
                ...         "username": StringType,
                ...         "email": StringType,
                ...         "age": IntegerType,
                ...         "account_balance": FloatType
                ...     }
                ... ).StringValidation.PatternMatch(
                ...     column="email",
                ...     pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                ...     impact="high"
                ... ).ValuesValidation.ColumnValuesToBeBetween(
                ...     column="age",
                ...     min_value=18,
                ...     max_value=120,
                ...     impact="high"
                ... ).StringValidation.LengthToBeBetween(
                ...     column="username",
                ...     min_value=3,
                ...     max_value=20,
                ...     impact="high"
                ... )
                >>>
                >>> # This should raise ValueError due to high impact failures
                >>> try:
                ...     vd_invalid.validate(raise_results=True)
                ... except ValueError as e:
                ...     print("Validation failed with multiple high impact errors")
                Validation failed with multiple high impact errors

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

            Parameters
              column_list (list | tuple): List or tuple of column names to check for
                  unique combinations.
              threshold (float, optional): Threshold for validation. Defaults to 0.0.
              impact (Literal["low", "medium", "high"], optional): Impact level of
                  validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with composite keys
                >>> df = pd.DataFrame({
                ...     "student_id": [101, 102, 103, 104, 105],
                ...     "course_id": [201, 202, 203, 204, 205],
                ...     "first_name": ["John", "Jane", "Alice", "Bob", "John"],
                ...     "last_name": ["Smith", "Doe", "Johnson", "Brown", "Williams"],
                ...     "grade": ["A", "B", "A+", "C", "B+"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate student_id and course_id combination is unique
                >>> vd = Validate(frame)
                >>> vd.UniqueValidation.ColumnUniquePair(
                ...     column_list=["student_id", "course_id"]
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should pass as all pairs are unique
                >>> key = "ColumnUniquePair_student_id_course_id"
                >>> assert vd.results[key]["result"]["status"] == "Success"
                >>>
                >>> # Validate first_name and last_name combination is unique
                >>> vd_names = Validate(frame)
                >>> vd_names.UniqueValidation.ColumnUniquePair(
                ...     column_list=["first_name", "last_name"]
                ... )
                >>>
                >>> # Execute validation
                >>> vd_names.validate()
                >>>
                >>> # Should pass as all name combinations are unique
                >>> key_names = "ColumnUniquePair_first_name_last_name"
                >>> assert vd_names.results[key_names]["result"]["status"] == "Success"
                >>>
                >>> # Create dataframe with duplicate pairs
                >>> df_duplicates = pd.DataFrame({
                ...     "student_id": [101, 102, 103, 101, 105],  # Duplicate student-course pair
                ...     "course_id": [201, 202, 203, 201, 205],   # Duplicate student-course pair
                ...     "first_name": ["John", "Jane", "Alice", "Bob", "Charlie"],
                ...     "last_name": ["Smith", "Doe", "Johnson", "Brown", "Smith"]
                ... })
                >>> frame_duplicates = nw.from_native(df_duplicates)
                >>>
                >>> # Apply validation to dataframe with duplicates
                >>> vd_duplicates = Validate(frame_duplicates)
                >>> vd_duplicates.UniqueValidation.ColumnUniquePair(
                ...     column_list=["student_id", "course_id"]
                ... ).UniqueValidation.ColumnUniquePair(
                ...     column_list=["first_name", "last_name"]
                ... )
                >>>
                >>> # Execute validation
                >>> vd_duplicates.validate()
                >>>
                >>> # Should fail for student-course pairs
                >>> assert vd_duplicates.results[key]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some duplicates
                >>> vd_threshold = Validate(frame_duplicates)
                >>> vd_threshold.UniqueValidation.ColumnUniquePair(
                ...     column_list=["student_id", "course_id"],
                ...     threshold=0.2  # Allow 20% duplicate pairs
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results[key]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with varying cardinality
                >>> df = pd.DataFrame({
                ...     "customer_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                ...     "product_category": ["A", "B", "C", "A", "B", "C", "A", "B", "C", "D"],
                ...     "payment_method": ["credit", "credit", "debit", "credit", "credit",
                ...                        "credit", "credit", "credit", "credit", "debit"],
                ...     "status": ["completed", "completed", "completed", "completed", "completed",
                ...                "completed", "completed", "completed", "completed", "completed"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate between 3-5 product categories
                >>> vd = Validate(frame)
                >>> vd.UniqueValidation.ColumnUniqueValueCountToBeBetween(
                ...     column="product_category",
                ...     min_value=3,
                ...     max_value=5
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should pass with 4 unique categories
                >>> key = "ColumnUniqueValueCountToBeBetween_product_category"
                >>> assert vd.results[key]["result"]["status"] == "Success"
                >>>
                >>> # Validate at least 3 payment methods - should fail
                >>> vd_payment = Validate(frame)
                >>> vd_payment.UniqueValidation.ColumnUniqueValueCountToBeBetween(
                ...     column="payment_method",
                ...     min_value=3
                ... )
                >>>
                >>> # Execute validation
                >>> vd_payment.validate()
                >>>
                >>> # Should fail with only 2 payment methods
                >>> key_payment = "ColumnUniqueValueCountToBeBetween_payment_method"
                >>> assert vd_payment.results[key_payment]["result"]["status"] == "Fail"
                >>>
                >>> # Validate status - should fail due to too few unique values
                >>> vd_status = Validate(frame)
                >>> vd_status.UniqueValidation.ColumnUniqueValueCountToBeBetween(
                ...     column="status",
                ...     min_value=2,
                ...     max_value=5
                ... )
                >>>
                >>> # Execute validation
                >>> vd_status.validate()
                >>>
                >>> # Should fail with only 1 unique status
                >>> key_status = "ColumnUniqueValueCountToBeBetween_status"
                >>> assert vd_status.results[key_status]["result"]["status"] == "Fail"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with categorical data
                >>> df = pd.DataFrame({
                ...     "status": ["active", "inactive", "pending", "active", "active",
                ...                "inactive", "active", "pending", "inactive", "active"],
                ...     "country": ["US", "CA", "UK", "US", "AU", "FR", "DE", "UK", "CA", "US"],
                ...     "user_type": ["admin", "regular", "guest", "regular", "regular",
                ...                   "admin", "admin", "guest", "regular", "super_admin"]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate status is one of the allowed values
                >>> vd = Validate(frame)
                >>> vd.UniqueValidation.ColumnUniqueValuesToBeInList(
                ...     column="status",
                ...     values=["active", "inactive", "pending"]
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should pass with all statuses in the allowed list
                >>> key = "ColumnUniqueValuesToBeInList_status"
                >>> assert vd.results[key]["result"]["status"] == "Success"
                >>>
                >>> # Validate user_type is one of the allowed values
                >>> vd_user = Validate(frame)
                >>> vd_user.UniqueValidation.ColumnUniqueValuesToBeInList(
                ...     column="user_type",
                ...     values=["admin", "regular", "guest"]
                ... )
                >>>
                >>> # Execute validation
                >>> vd_user.validate()
                >>>
                >>> # Should fail with 'super_admin' not in the allowed list
                >>> key_user = "ColumnUniqueValuesToBeInList_user_type"
                >>> assert vd_user.results[key_user]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some values outside the list
                >>> vd_threshold = Validate(frame)
                >>> vd_threshold.UniqueValidation.ColumnUniqueValuesToBeInList(
                ...     column="user_type",
                ...     values=["admin", "regular", "guest"],
                ...     threshold=0.25  # Allow 25% values outside list
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results[key_user]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with numeric values
                >>> df = pd.DataFrame({
                ...     "age": [25, 30, 42, 18, 65, 55, 37, 29, 50, 70],
                ...     "score": [85, 92, 78, 65, 100, 88, 72, 95, 80, 91],
                ...     "temperature": [98.6, 99.1, 97.8, 100.2, 98.9, 101.5,
                ...                     97.5, 98.8, 99.5, 98.2]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate ages are between 18 and 65
                >>> vd = Validate(frame)
                >>> vd.ValuesValidation.ColumnValuesToBeBetween(
                ...     column="age",
                ...     min_value=18,
                ...     max_value=65
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should fail with one age above 65
                >>> key = "ColumnValuesToBeBetween_age"
                >>> assert vd.results[key]["result"]["status"] == "Fail"
                >>>
                >>> # Validate scores are at least 60
                >>> vd_score = Validate(frame)
                >>> vd_score.ValuesValidation.ColumnValuesToBeBetween(
                ...     column="score",
                ...     min_value=60
                ... )
                >>>
                >>> # Execute validation
                >>> vd_score.validate()
                >>>
                >>> # Should pass with all scores above 60
                >>> key_score = "ColumnValuesToBeBetween_score"
                >>> assert vd_score.results[key_score]["result"]["status"] == "Success"
                >>>
                >>> # Validate temperatures with threshold
                >>> vd_temp = Validate(frame)
                >>> vd_temp.ValuesValidation.ColumnValuesToBeBetween(
                ...     column="temperature",
                ...     min_value=97.0,
                ...     max_value=100.0,
                ...     threshold=0.2  # Allow 20% outside range
                ... )
                >>>
                >>> # Execute validation
                >>> vd_temp.validate()
                >>>
                >>> # Should pass with threshold
                >>> key_temp = "ColumnValuesToBeBetween_temperature"
                >>> assert vd_temp.results[key_temp]["result"]["status"] == "Success"
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
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with budget allocation
                >>> df = pd.DataFrame({
                ...     "project_id": [1, 2, 3, 4, 5],
                ...     "hardware_budget": [5000, 8000, 10000, 7500, 12000],
                ...     "software_budget": [3000, 5000, 8000, 4500, 6000],
                ...     "personnel_budget": [12000, 15000, 22000, 18000, 27000],
                ...     "total_budget": [20000, 28000, 40000, 30000, 45000]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate that component budgets sum to total budget
                >>> vd = Validate(frame)
                >>> # For each row, check all projects
                >>> for i in range(len(df)):
                ...     project_frame = nw.from_native(df.iloc[[i]])
                ...     vd_project = Validate(project_frame)
                ...     vd_project.ValuesValidation.ColumnsSumToBeEqualTo(
                ...         columns_list=["hardware_budget", "software_budget", "personnel_budget"],
                ...         sum_value=df.iloc[i]["total_budget"]
                ...     )
                ...     vd_project.validate()
                ...     key = "ColumnsSumToBeEqualTo_hardware_budget_software_budget_personnel_budget"
                ...     assert vd_project.results[key]["result"]["status"] == "Success"
                >>>
                >>> # Create dataframe with incorrect totals
                >>> df_incorrect = pd.DataFrame({
                ...     "project_id": [1, 2, 3],
                ...     "hardware_budget": [5000, 8000, 10000],
                ...     "software_budget": [3000, 5000, 8000],
                ...     "personnel_budget": [12000, 15000, 22000],
                ...     "total_budget": [21000, 28000, 42000]  # Incorrect totals
                ... })
                >>> frame_incorrect = nw.from_native(df_incorrect)
                >>>
                >>> # Check project 1 - should fail
                >>> project1 = nw.from_native(df_incorrect.iloc[[0]])
                >>> vd_incorrect = Validate(project1)
                >>> vd_incorrect.ValuesValidation.ColumnsSumToBeEqualTo(
                ...     columns_list=["hardware_budget", "software_budget", "personnel_budget"],
                ...     sum_value=df_incorrect.iloc[0]["total_budget"]
                ... )
                >>>
                >>> # Execute validation
                >>> vd_incorrect.validate()
                >>>
                >>> # Should fail with incorrect sum
                >>> key = "ColumnsSumToBeEqualTo_hardware_budget_software_budget_personnel_budget"
                >>> assert vd_incorrect.results[key]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some difference
                >>> vd_threshold = Validate(project1)
                >>> vd_threshold.ValuesValidation.ColumnsSumToBeEqualTo(
                ...     columns_list=["hardware_budget", "software_budget", "personnel_budget"],
                ...     sum_value=df_incorrect.iloc[0]["total_budget"],
                ...     threshold=0.05  # Allow 5% difference
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold (difference is about 4.8%)
                >>> assert vd_threshold.results[key]["result"]["status"] == "Success"
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
                max_sum_value (float | None): Minimum sum value that columns should be
                    greater than or equal to.
                min_sum_value (float | None): Maximum sum value that columns should be
                    less than or equal to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (Literal["low", "medium", "high"], optional): Impact level of
                    validation. Defaults to "low".

            Examples:
                >>> import pandas as pd
                >>> import narwhals as nw
                >>> from validoopsie import Validate
                >>>
                >>> # Create test dataframe with ingredient nutritional info
                >>> df = pd.DataFrame({
                ...     "ingredient": ["Beef", "Chicken", "Salmon", "Tofu", "Eggs"],
                ...     "protein": [26, 31, 25, 8, 13],
                ...     "fat": [19, 4, 13, 4, 11],
                ...     "carbs": [0, 0, 0, 2, 1]
                ... })
                >>> frame = nw.from_native(df)
                >>>
                >>> # Validate total macronutrients are between 30-50g
                >>> vd = Validate(frame)
                >>> vd.ValuesValidation.ColumnsSumToBeBetween(
                ...     columns_list=["protein", "fat", "carbs"],
                ...     min_sum_value=30,
                ...     max_sum_value=50
                ... )
                >>>
                >>> # Execute validation
                >>> vd.validate()
                >>>
                >>> # Should pass with all sums in range
                >>> key = "ColumnsSumToBeBetween_protein_fat_carbs"
                >>> assert vd.results[key]["result"]["status"] == "Success"
                >>>
                >>> # Create dataframe with values outside the range
                >>> df_outside = pd.DataFrame({
                ...     "ingredient": ["Rice", "Bread", "Pasta", "Potato", "Beans"],
                ...     "protein": [3, 4, 5, 2, 9],
                ...     "fat": [0, 1, 1, 0, 0],
                ...     "carbs": [28, 23, 25, 17, 27]
                ... })
                >>> frame_outside = nw.from_native(df_outside)
                >>>
                >>> # Apply same validation
                >>> vd_outside = Validate(frame_outside)
                >>> vd_outside.ValuesValidation.ColumnsSumToBeBetween(
                ...     columns_list=["protein", "fat", "carbs"],
                ...     min_sum_value=30,
                ...     max_sum_value=50
                ... )
                >>>
                >>> # Execute validation
                >>> vd_outside.validate()
                >>>
                >>> # Some items have totals below 30, should fail
                >>> assert vd_outside.results[key]["result"]["status"] == "Fail"
                >>>
                >>> # With threshold allowing some values outside range
                >>> vd_threshold = Validate(frame_outside)
                >>> vd_threshold.ValuesValidation.ColumnsSumToBeBetween(
                ...     columns_list=["protein", "fat", "carbs"],
                ...     min_sum_value=30,
                ...     max_sum_value=50,
                ...     threshold=0.4  # Allow 40% outside range
                ... )
                >>>
                >>> # Execute validation
                >>> vd_threshold.validate()
                >>>
                >>> # Should pass with threshold
                >>> assert vd_threshold.results[key]["result"]["status"] == "Success"
            """

