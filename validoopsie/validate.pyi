from typing import Any, Union

from narwhals.typing import IntoFrame

from validoopsie.types import KwargsType

class Validate:
    frame: IntoFrame
    results: dict[str, Any]
    def __init__(self, frame: IntoFrame) -> None: ...
    def validate(self) -> Validate: ...

    class DateValidation:
        @staticmethod
        def ColumnMatchDateFormat(
            column: str,
            date_format: str,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column match the date format.

            Args:
                column (str): Column to validate.
                date_format (str): Date format to check.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

    class EqualityValidation:
        @staticmethod
        def PairColumnEquality(
            column: str,
            target_column: str,
            group_by_combined: bool = True,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the pair of columns are equal.

            Args:
                column (str): Column to validate.
                target_column (str): Column to compare.
                group_by_combined (bool, optional): Group by combine columns.
                    Default True.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

    class NullValidation:
        @staticmethod
        def ColumnBeNull(
            column: str,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are null.

            Args:
                column (str): Column to validate.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnNotBeNull(
            column: str,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are not null.

            Args:
                column (str): Column to validate.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

    class ValuesValidation:
        @staticmethod
        def ColumnUniqueValuesToBeInList(
            column: str,
            values: list[Union[str, float, int]],
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the unique values are in the list.

            Args:
                column (str): Column to validate.
                values (list[str | float | int]): List of values to check.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnValuesToBeBetween(
            column: str,
            min_value: int,
            max_value: int,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are between a range.

            Args:
                column (str): Column to validate.
                min_value (int): Minimum value.
                max_value (int): Maximum value.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnsSumToBeEqualTo(
            columns_list: list[str],
            sum_value: int,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the sum of the columns is equal to a specific value.

            Args:
                columns_list (list[str]): List of columns to sum.
                sum_value (float): Value that the columns should sum to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnsSumToBeGreaterEqualTo(
            columns_list: list[str],
            max_sum: float,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the sum of columns greater or equal than `max_sum`.

            Args:
                columns_list (list[str]): List of columns to sum.
                max_sum (float): Max sum value that column should less or equal to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """

        @staticmethod
        def ColumnsSumToBeLessEqualTo(
            columns_list: list[str],
            min_sum: float,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the sum of columns less or equal than `min_sum`.

            Args:
                columns_list (list[str]): List of columns to sum.
                min_sum (float): Min sum value that column should greater or equal to.
                threshold (float, optional): Threshold for validation. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs:KwargsType (dict): Additional keyword arguments.

            """
