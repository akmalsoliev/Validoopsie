# Developing a Custom Validation

In certain situations, the default validations may not be sufficient to check
the quality of your data, especially when dealing with complex cases. To handle
these scenarios, you can develop your own custom validation that encapsulates
the specific logic required for your data quality checks.

This guide will walk you through the process of developing a custom validation
using the Validoopsie library.

## Final Output

```py
from typing import Literal
from validoopsie.base import BaseValidation
from narwhals.typing import FrameT

class MyCustomValidation(BaseValidation):
    """Custom validation that filters temperature data based on grouped dates.

    Args:
        column (str): The column name used in the validation and as an identifier in results.
        threshold (float, optional): The threshold for the validation. Defaults to 0.0.
        impact (str, optional): The impact level of the validation. Defaults to "low".
        kwargs (dict): Additional keyword arguments.

    """
    def __init__(
        self,
        column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message used in the report."""
        return "Custom validation failed: Temperature readings are outside acceptable ranges."

    def __call__(self, frame: FrameT) -> FrameT:
        """Execute the custom validation logic.

        Args:
            frame (FrameT): The data frame to validate.

        Returns:
            FrameT: A data frame containing records that failed the validation.
        """
        return (
            frame.group_by(self.column)
            .agg(nw.col("temperature").mean().alias("mean_temperature_farenheit"))
            .with_columns(
                ((nw.col("mean_temperature_farenheit") - 32) * 5 / 9).alias(
                    "mean_temperature_celsius",
                ),
            )
            .filter(
                # Every tempearture above 60 degrees celsius is considered as an error
                nw.col("mean_temperature_celsius") > 60,
                # Every tempearture below -40 degrees celsius is considered as an error
                nw.col("mean_temperature_celsius") < -40,
                # Every mean tempearture below -10 and above 30 degrees celsius is considered as an error
                nw.col("mean_temperature_celsius").is_between(-10, 30) == False,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )

```

## 1. Define the Validation Class

To create a custom validation, start by defining a new class that inherits from
`BaseValidation`:

```python
from typing import Literal
from validoopsie.base import BaseValidation
from narwhals.typing import FrameT

class MyCustomValidation(BaseValidation):
```

## 2. Add a Docstring

While not strictly required, adding a docstring is best practice, especially for
team collaboration and future maintenance. The docstring should describe the
purpose of the validation and explain the parameters.

Example:

```python
"""Custom validation that filters temperature data based on grouped dates.

Args:
    column (str): The column name used in the validation and as an identifier in results.
    threshold (float, optional): The threshold for the validation. Defaults to 0.0.
    impact (str, optional): The impact level of the validation. Defaults to "low".
    kwargs (dict): Additional keyword arguments.

"""
```

## 3. Define the `__init__` Method

The `__init__` method initializes your validation class. It should include at
least the `column` parameter, along with impact and threshold parameters. The
base class requires these parameters to be passed explicitly.

Example:

```python
    def __init__(
        self,
        column: str,
        impact: Literal["low", "medium", "high"] = "low",
        threshold: float = 0.00,
    ) -> None:
        super().__init__(column, impact, threshold, **kwargs)
```

## 4. Add a Fail Message

The fail message is used in the output report if the validation fails. Define it
using a property method to provide a meaningful message that aids in diagnosing
issues.

Example:

```python
    @property
    def fail_message(self) -> str:
        """Return the fail message used in the report."""
        return "Custom validation failed: Temperature readings are outside acceptable ranges."
```

## 5. Define the Validation Logic (`__call__` Method)

The `__call__` method contains the core logic of your validation. This method
should return only the records that do not meet the validation criteria.

Example:

```python
    def __call__(self, frame: FrameT) -> FrameT:
        """Execute the custom validation logic.

        Args:
            frame (FrameT): The data frame to validate.

        Returns:
            FrameT: A data frame containing records that failed the validation.
        """
        return (
            frame.group_by(self.column)
            .agg(nw.col("temperature").mean().alias("mean_temperature_farenheit"))
            .with_columns(
                ((nw.col("mean_temperature_farenheit") - 32) * 5 / 9).alias(
                    "mean_temperature_celsius",
                ),
            )
            .filter(
                # Every tempearture above 60 degrees celsius is considered as an error
                nw.col("mean_temperature_celsius") > 60,
                # Every tempearture below -40 degrees celsius is considered as an error
                nw.col("mean_temperature_celsius") < -40,
                # Every mean tempearture below -10 and above 30 degrees celsius is considered as an error
                nw.col("mean_temperature_celsius").is_between(-10, 30) == False,
            )
            .group_by(self.column)
            .agg(nw.col(self.column).count().alias(f"{self.column}-count"))
        )
```

**Notes:**

- Ensure that the logic correctly identifies and returns only the failing
  records.

## 6. Add the Validation to the Pipeline

To integrate your custom validation into the data validation pipeline, use the
`add_validation` method of the `Validate` class.

Example:

```python
import pandas as pd
from validoopsie import Validate

# Sample data frame
df = pd.DataFrameT({
    "date": ['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01'],
    "temperature": [50, 60, 70, 80],
})

# Initialize the Validate object
validator = Validate(df)

# Add your custom validation
validator.add_validation(MyCustomValidation(column="date"))

# Access the results directly
result = validator.results

print(result)
```

## 7. Example Output

After running the validation, you can expect an output similar to the following:

```json
{
  "Summary": {
    "passed": true,
    "validations": ["MyCustomValidation_date"]
  },
  "MyCustomValidation_date": {
    "validation": "MyCustomValidation",
    "impact": "low",
    "timestamp": "2025-01-10T17:54:14.035378+01:00",
    "column": "date",
    "result": {
      "status": "Success",
      "threshold pass": true,
      "message": "All items passed the validation.",
      "frame row number": 4,
      "threshold": 0.0
    }
  }
}
```

---

With this guide, you should be able to create custom validations tailored to
your specific data quality requirements. Remember to thoroughly test your custom
validation to ensure it behaves as expected in all scenarios.
