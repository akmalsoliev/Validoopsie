# Impact Levels in Validoopsie

Validoopsie uses impact levels to determine how validation failures should be handled. Properly setting the impact level helps control the behavior of your data validation pipeline.

## Available Impact Levels

Validoopsie supports three impact levels:

| Level | Description | Behavior |
|-------|-------------|----------|
| `"low"` | Minor validation issues that don't significantly affect data quality | Records failures in results but doesn't interrupt processing |
| `"medium"` | Moderate validation issues that may affect data quality | Records failures in results but doesn't interrupt processing |
| `"high"` | Critical validation issues that severely affect data quality | Raises a `ValueError` exception when `.validate()` is called |

## How to Set Impact Levels

Impact levels can be set on any validation:

```python
from validoopsie import Validate
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "value": [10, 20, 30, 200, 40]
})

validator = Validate(df)

# Low impact - will be recorded but won't raise exceptions
validator.ValuesValidation.ColumnValuesToBeBetween(
    column="value", 
    min_value=0, 
    max_value=100,
    impact="low"  # This is the default if not specified
)

# Medium impact - generally used for important but not critical validations
validator.TypeValidation.TypeCheck(
    column="id",
    type_name="int64",
    impact="medium"
)

# High impact - will raise an exception when validate() is called
validator.NullValidation.ColumnNotBeNull(
    column="id",
    impact="high"  # This will cause validate() to raise an exception if nulls are found
)

# This will raise an exception if any high-impact validations fail
try:
    validator.validate()
except ValueError as e:
    print(f"Validation failed: {e}")
```

## When to Use Each Impact Level

- **Low**: Use for informational validations or when failures can be tolerated
    - Example: Checking if string values follow a preferred format
    - Example: Verifying that numerical values fall within suggested (but not required) ranges

- **Medium**: Use for important validations where failures should be highlighted
    - Example: Checking if dates fall within an expected range
    - Example: Verifying that categorical values belong to an expected set

- **High**: Use for critical validations where failures should interrupt processing
    - Example: Ensuring primary key columns don't contain null values
    - Example: Verifying that required fields are present
    - Example: Checking data integrity constraints that must be satisfied

## Default Impact Level

If not specified, all validations default to an impact level of `"low"`.
