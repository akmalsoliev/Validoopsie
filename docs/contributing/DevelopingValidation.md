# Contributing a new Validation to Validoopsie

Creating a new validation might seem complex at first, but don’t worry—we’ve
made the process as straightforward as possible. Validations are dynamically
imported from the `validoopsie/validation_catalogue` directory, and once you
create your first one, everything will start to make sense!

Follow these steps to create a new validation:

---

## 1. Organize Your Validation

In the `validoopsie/validation_catalogue` directory, validations are organized
by category. For this example, we’ll create a validation to check whether
values in a column fall between two numbers.

Since this is a value-based validation, you’ll create the file inside the
`ValuesValidation` folder.

---

## 2. Create the Validation File

1. Create a new file in `validoopsie/validation_catalogue/ValuesValidation`.
2. Name the file using this convention:
   **File Name**: `column_values_to_be_between.py`
   **Class Name**: `ColumnValuesToBeBetween`

---

## 3. Define the Validation Class

Your class should inherit from `BaseValidation`.

Here’s an example:

```python
from validoopsie.base import BaseValidation
# We will use these later
from typing import Literal
from narwhals.typing import Frame

class ColumnValuesToBeBetween(BaseValidation):
```

---

## 4. Add a Docstring

Include a clear docstring and doctest for both the class and its methods, these will also be 
reused for the stub file later on. Here’s an example structure:

```python
"""Check if the values in a column are within a specific range.

Args:
    column (str): Column to validate.
    min_value (int): Minimum value.
    max_value (int): Maximum value.
    threshold (float, optional): Validation threshold. Defaults to 0.0.
    impact (str, optional): Impact level of validation. Defaults to "low".
    kwargs (dict): Additional keyword arguments.

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
```

Doctest servers as a double purpose, it provides examples on how to use the validation, 
automatically showcased in the documentation and also serves as a test case for the 
validation.

---

## 5. Implement the `__init__` Method

The `__init__` method must include `column` (if your validation uses a
combination of columns or some other varation pass it later to
`super().__init__`).

In this case we are attempting to find values between two numbers, hence, these
parameters are required: `column`, `min_value`, and `max_value`.
It should also include the standard `impact` and `threshold` parameters
required by the base class (`BaseValidation`).

- Always pass `column`, `impact`, and `threshold` to the base class.
- If your validation doesn’t require a column, generate one in the `__init__` method.

Example:

```python
def __init__(
    self,
    column: str,
    min_value: float,
    max_value: float,
    impact: Literal["low", "medium", "high"] = "low",
    threshold: float = 0.00,
    **kwargs: dict[str, object],
) -> None:
    super().__init__(column, impact, threshold, **kwargs)
    self.min_value = min_value
    self.max_value = max_value
```

---

## 6. Add a Fail Message

The fail message is included in the output report if the validation fails.
Define it using a property:

```python
@property
def fail_message(self) -> str:
    """Return the fail message used in the report."""
    return (
        f"The column '{self.column}' has values that are not "
        f"between {self.min_value} and {self.max_value}."
    )
```

---

## 7. Define the Validation Logic (`__call__` Method)

The `__call__` method contains the core logic of your validation. It should
return only the failed values.

Example:

```python
def __call__(self, frame: Frame) -> Frame:
    """Check if the values in a column are within the specified range.

    The result will be used during execution.
    """
    return (
        frame.group_by(self.column)
        .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        .filter(
            nw.col(self.column).is_between(self.min_value, self.max_value) == False,
        )
    )
```

---

## 8. Test Your Validation

Prior to proceeding with test generation, you might want to use your already generated test in the docstring, for that you can run:
```bash
    uv run pytest validoopsie --doctest-modules
```

1. Create a test file under `tests/test_validation_catalogue/test_ValuesValidation`.
2. Use the `@create_frame_fixture` decorator to define test data for different
   DataFrame libraries (`pandas`, `polars`, `pyarrow`, etc.).

Example:

```python
from tests.utils.create_frames import create_frame_fixture

@create_frame_fixture
def lf() -> dict[str, list]:
    return {
        "A": [1, 2, 3, 4, 5],
        "B": [1.0, 2.0, 3.0, 4.0, 5.0],
    }
```

3. Write test cases for your validation:

```python
def test_column_values_to_be_between(lf: Frame) -> None:
    test = ColumnValuesToBeBetween("A", 1, 2)
    result = test.__execute_check__(frame=lf)
    assert result["result"]["status"] == "Fail"
```

---

## 9. Update the Stub File for Type Hinting

To enable proper type hinting for your new validation, update the stub file
(`validate.pyi`). This step is essential because validations are dynamically
imported.

Add your validation like this:

```python
class Validate:
    class ValuesValidation:
        @staticmethod
        def ColumnValuesToBeBetween(
            column: str,
            min_value: int,
            max_value: int,
            threshold: float = 0.00,
            impact: str = "low",
            **kwargs: KwargsType,
        ) -> Validate:
            """Check if the values in a column are within a specific range.

            Args:
                column (str): Column to validate.
                min_value (int): Minimum value.
                max_value (int): Maximum value.
                threshold (float, optional): Validation threshold. Defaults to 0.0.
                impact (str, optional): Impact level of validation. Defaults to "low".
                kwargs (dict): Additional keyword arguments.

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
```

Make sure to include a docstring here as well since they’re dynamically imported.

---

## All Done!

Congratulations! You’ve just created your first validation. 🎉

If you have any questions or run into issues, feel free to reach out for help.
Thank you for contributing!
