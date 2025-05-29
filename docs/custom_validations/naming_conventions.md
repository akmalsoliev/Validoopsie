# Naming Conventions for Custom Validations

When creating custom validations for Validoopsie, following a consistent naming convention helps maintain code readability and ensures your validations integrate seamlessly with the library. This guide outlines the recommended naming patterns.

## Class Naming Convention

Custom validation classes should follow PascalCase (also known as UpperCamelCase) naming:

```python
class ColumnValuesToBeBetween(BaseValidationParameters):
    # Implementation
```

The class name should be descriptive and indicate:

1. What is being validated (e.g., "Column", "DataType", "String")

2. The type of validation (e.g., "ToBeBetween", "NotBeNull", "Match")

## File Naming Convention

Files containing validation classes should follow snake_case naming and match the class name:

- Class: `ColumnValuesToBeBetween`
- File: `column_values_to_be_between.py`

## Naming Patterns by Validation Type

Follow these patterns for different types of validations:

### Value Validations

- `ColumnValuesToBeEqual` - Check if values equal a specific value
- `ColumnValuesToBeBetween` - Check if values fall within a range
- `ColumnValuesToBeGreaterThan` - Check if values exceed a threshold

### String Validations

- `PatternMatch` - Check if strings match a regex pattern
- `NotPatternMatch` - Check if strings don't match a regex pattern
- `LengthToBeEqual` - Check if string length equals a specific value
- `LengthToBeBetween` - Check if string length falls within a range

### Null Validations

- `ColumnBeNull` - Check if values are null
- `ColumnNotBeNull` - Check if values are not null

### Type Validations

- `TypeCheck` - Check if values are of a specific type

### Date Validations

- `DateToBeBetween` - Check if dates fall within a range
- `ColumnMatchDateFormat` - Check if date strings match a format

## Organizing Custom Validations

Organize your custom validations in a logical category structure:

```
my_project/
├── validations/
│   ├── __init__.py
│   ├── date_validations/
│   │   ├── __init__.py
│   │   └── fiscal_quarter_match.py
│   ├── string_validations/
│   │   ├── __init__.py
│   │   └── country_code_match.py
│   └── custom_validations/
│       ├── __init__.py
│       └── business_rule_check.py
```

## Registering Custom Validations

When registering custom validations with Validoopsie, use a descriptive name that follows the same convention:

```python
from validoopsie import Validate
from my_project.validations.custom_validations.business_rule_check import BusinessRuleCheck

# Create validator instance
validator = Validate(df)

# Add custom validation
validator.add_validation(BusinessRuleCheck(column="transaction_type", impact="high"))
```

## Examples of Well-Named Custom Validations

### Good Examples:

- `TransactionIdsUnique` - Checks if transaction IDs are unique
- `CustomerCodeMatchPattern` - Validates customer code format
- `DateWithinFiscalYear` - Ensures dates fall within fiscal year
- `AmountSumEqualsTotal` - Verifies that amounts sum to expected total

### Poor Examples (Avoid):

- `Check1` - Too vague
- `ValidateThis` - Doesn't describe what's being validated
- `MyCustomVal` - Not descriptive
- `DoStuff` - Doesn't explain the validation purpose

## Type Hinting for Custom Validations

When adding type hints, follow this pattern:

```python
    def __init__(
        self,
        column: str,
        pattern: str,
        threshold: float = 0.0,
        impact: Literal["low", "medium", "high"] = "low",
    ) -> None:
        # Implementation
```

By following these naming conventions, you ensure that your custom validations are easily understood by other developers and integrate well with Validoopsie's existing validation structure.
