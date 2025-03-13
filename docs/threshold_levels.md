# Threshold Levels in Validoopsie

Validoopsie uses threshold arguments to specify the acceptable failure rate
before a validation fails. This allows for more flexible validation rules that
can tolerate a certain percentage of exceptions.

## Understanding Thresholds

Thresholds in Validoopsie represent the maximum allowable percentage of records that can fail validation:

| Threshold | Description | Behavior |
|-----------|-------------|----------|
| `0.0` | No failures allowed (default) | Validation fails if any records don't meet criteria |
| `0.1` | 10% failure tolerance | Validation passes if 90% or more records meet criteria |
| `0.5` | 50% failure tolerance | Validation passes if at least half of records meet criteria |
| `1.0` | 100% failure tolerance | Validation always passes regardless of failures |

## How to Set Thresholds

Thresholds can be set on any validation:

```python
from validoopsie import Validate
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "value": [10, 20, 30, 200, 40]
})

validator = Validate(df)

# No tolerance - fails if any values are outside range
validator.ValuesValidation.ColumnValuesToBeBetween(
    column="value", 
    min_value=0, 
    max_value=100,
    threshold=0.0  # This is the default if not specified
)

# 20% tolerance - passes if at least 80% of values are within range
validator.ValuesValidation.ColumnValuesToBeBetween(
    column="value", 
    min_value=0, 
    max_value=100,
    threshold=0.2
)

# Combine with impact levels for complete validation control
validator.StringValidation.PatternMatch(
    column="email",
    pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    threshold=0.05,  # Allow 5% of emails to be invalid
    impact="medium"  # Record failures but don't interrupt processing
)
```

## When to Use Thresholds

- **Zero Threshold (0.0)**: Use for strict validations where no exceptions are allowed
    - Example: Primary key uniqueness
    - Example: Required fields that must be present

- **Low Threshold (< 0.1)**: Use for validations that should generally pass but can tolerate rare exceptions
    - Example: Email format validation that might have a few legacy exceptions
    - Example: Date format validation with occasional special cases

- **Medium Threshold (0.1 - 0.5)**: Use when a significant portion of data might legitimately fail validation
    - Example: Missing values in optional fields
    - Example: Pattern matching for fields with multiple valid formats

- **High Threshold (> 0.5)**: Use rarely, typically for informational validations
    - Example: Checking if most records follow a new standard that's being gradually implemented
    - Example: Monitoring the adoption rate of new data formats

## Default Threshold

If not specified, all validations default to a threshold of `0.0` (no failures allowed).
