<h1 align="center">
    <img width="400" alt="validoopsie" src="https://github.com/akmalsoliev/Validoopsie/blob/14ac7fff59d8e02f6af61c22991888064a45575a/assets/validoopsie-text.png?raw=true">
    <p style="font-size: 16px; font-weight: bold;">A simple and easy to use Data Validation library for Python.</p>
    <img width="400" alt="validoopsie" src="https://github.com/akmalsoliev/Validoopsie/blob/14ac7fff59d8e02f6af61c22991888064a45575a/assets/logo.png?raw=true">
</h1>

<p align="center">
  <a href="https://badge.fury.io/py/Validoopsie">
    <img src="https://badge.fury.io/py/Validoopsie.svg" alt="PyPI version" />
  </a>
  <a href="https://pepy.tech/projects/validoopsie">
    <img src="https://static.pepy.tech/badge/validoopsie" alt="PyPI Downloads">
  </a>
  <a href="https://www.repostatus.org/#active">
    <img src="https://www.repostatus.org/badges/latest/active.svg" alt="Repo Status">
  </a>
  <a href="https://github.com/akmalsoliev/Validoopsie/actions/workflows/pytest-ruff.yaml">
    <img src="https://github.com/akmalsoliev/Validoopsie/actions/workflows/pytest-ruff.yaml/badge.svg" alt="Tests and Linters" />
  </a>
  <a href="https://github.com/akmalsoliev/Validoopsie/actions/workflows/docs.yaml">
    <img src="https://github.com/akmalsoliev/Validoopsie/actions/workflows/docs.yaml/badge.svg" alt="Documentation" />
  </a>
</p>

# Validoopsie

Validoopsie is a remarkably lightweight and user-friendly data validation
library for Python. It’s designed to help you easily declare classes and chain
validations together, in a style reminiscent of popular DataFrame libraries.
This makes it a familiar and intuitive tool for developers who regularly work
with dataframes.

Thanks to the excellent work by
[Narwhals](https://github.com/narwhals-dev/narwhals), Validoopsie incorporates
the "Bring Your Own DataFrame" (BYOD) concept. This flexibility allows you to
use any DataFrame that Narwhals supports for your data validation tasks. To
explore the full range of supported DataFrames, you can visit [this
link](https://narwhals-dev.github.io/narwhals/extending/).

The syntax of Validoopsie has been thoughtfully crafted to ensure ease of use.
Every validation function is encapsulated in its own method, which can be
seamlessly linked together. This method-specific design prioritizes simplicity
and readability, freeing you from the need to adapt to a new API each time you
switch libraries. It allows you to focus on maintaining clean and
understandable code.

Validoopsie draws significant inspiration from the Great Expectations library.
It strives to distill the data validation process into something
straightforward and efficient. Whether you're checking data integrity or
ensuring compliance with data standards, Validoopsie provides a streamlined yet
powerful solution to make these tasks accessible and straightforward.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Development](#development)
4. [License](#license)

## Installation

- pip

    `pip install Validoopsie`

## Getting Started

- [📖 Documentation](https://akmalsoliev.github.io/Validoopsie/)
- [🚨 Impact Levels in Validoopsie](https://akmalsoliev.github.io/Validoopsie/impact_levels.html)
- [🎯 Threshold Levels in Validoopsie](https://akmalsoliev.github.io/Validoopsie/threshold_levels.html)
- [🛠️ Contribution Guidelines](https://akmalsoliev.github.io/Validoopsie/contributing/CONTRIBUTING.html)
- [✨ Contributing a new Validation to Validoopsie](https://akmalsoliev.github.io/Validoopsie/contributing/DevelopingValidation.html)
- [🧑‍💻 Develop your own custom validation](https://akmalsoliev.github.io/Validoopsie/DevelopingValidationCustom.html)
- [🗂️ Validation Catalog](https://akmalsoliev.github.io/Validoopsie/validation_catalogue/Date%20Validation.html)

Validoopsie is incredibly easy to use, so much so that you could do it
half-asleep. The simplicity of the library is enhanced by the BYOD (Bring Your
Own DataFrame) concept, where you merely need to utilize the `Validate` class
and chain your desired validations together. This approach ensures that you can
get started with minimal effort and without any unnecessary complexity.

```py
import pandas as pd

from validoopsie import Validate

p_df = pd.DataFrame(
    {
        "name": ["John", "Doe", "Jane"],
        "target_name": ["John", "Doe", "Jane"],
        "last_name": ["Smith", "Smith", "Smith"],
        "age": [25, 30, 35],
    },
)

# `vd` stands for Validate Data
vd = Validate(p_df)
vd.EqualityValidation.PairColumnEquality(
    column="name",
    target_column="age",
    impact="high",
).UniqueValidation.ColumnUniqueValuesToBeInList(
    column="last_name",
    values=["Smith"],
).ValuesValidation.ColumnValuesToBeBetween(
    column="age",
    min_value=20,
    max_value=40,
)

vd.results
```

**OUTPUT:**

```json
{
    "Summary": {
        "passed": false,
        "validations": [
            "PairColumnEquality_name",
            "ColumnUniqueValuesToBeInList_last_name",
            "ColumnValuesToBeBetween_age"
        ],
        "failed_validation": [
            "PairColumnEquality_name"
        ]
    },
    "PairColumnEquality_name": {
        "validation": "PairColumnEquality",
        "impact": "high",
        "timestamp": "2025-03-17T10:28:08.258604+01:00",
        "column": "name",
        "result": {
            "status": "Fail",
            "threshold_pass": false,
            "message": "The column 'name' is not equal to the column'age'.",
            "failing_items": [
                "Doe - column name - column age - 30",
                "Jane - column name - column age - 35",
                "John - column name - column age - 25"
            ],
            "failed_number": 3,
            "frame_row_number": 3,
            "threshold": 0.0,
            "failed_percentage": 1.0
        }
    },
    "ColumnUniqueValuesToBeInList_last_name": {
        "validation": "ColumnUniqueValuesToBeInList",
        "impact": "low",
        "timestamp": "2025-03-17T10:28:08.265990+01:00",
        "column": "last_name",
        "result": {
            "status": "Success",
            "threshold_pass": true,
            "message": "All items passed the validation.",
            "frame_row_number": 3,
            "threshold": 0.0
        }
    },
    "ColumnValuesToBeBetween_age": {
        "validation": "ColumnValuesToBeBetween",
        "impact": "low",
        "timestamp": "2025-03-17T10:28:08.267564+01:00",
        "column": "age",
        "result": {
            "status": "Success",
            "threshold_pass": true,
            "message": "All items passed the validation.",
            "frame_row_number": 3,
            "threshold": 0.0
        }
    }
}
```

To ensure that all your validations have been correctly executed and to handle
any potential errors that may arise during the validation process, you can use
the `validate` method. However, it's important to note that errors will only be
raised if the `impact` level is set to `high`. Without this setting, potential
issues may not trigger an error message.

**NOTE:** Raised error is a custom `ValueError`.

```py
import pandas as pd

from validoopsie import Validate

p_df = pd.DataFrame(
    {
        "name": ["John", "Doe", "Jane"],
        "target_name": ["John", "Doe", "Jane"],
        "last_name": ["Smith", "Smith", "Smith"],
        "age": [25, 30, 35],
    },
)

# `vd` stands for Validate Data
vd = Validate(p_df)
vd.EqualityValidation.PairColumnEquality(
    column="name",
    target_column="age",
    impact="high",
).UniqueValidation.ColumnUniqueValuesToBeInList(
    column="last_name",
    values=["Smith"],
).ValuesValidation.ColumnValuesToBeBetween(
    column="age",
    min_value=20,
    max_value=40,
).validate()
```

Thanks to [loguru](https://github.com/Delgan/loguru) output will provide a very
condenced information on validations and their status in a colorful way.

<p align="left">
    <img width="1000" alt="validation output" src="https://github.com/akmalsoliev/Validoopsie/blob/14ac7fff59d8e02f6af61c22991888064a45575a/assets/validate.png?raw=true">
</p>

## Development

Validoopsie includes a Makefile to simplify development tasks:

```bash
# Install dependencies
make setup

# Run linters (mypy, ruff)
make lint

# Run tests (includes doctests, stubtest)
make test

# Run both lint and test
make all
```

For more information on development, check the [contribution guidelines](https://akmalsoliev.github.io/Validoopsie/contributing/CONTRIBUTING.html).

## License

MIT © Validoopsie

Original Creator - [Akmal Soliev](https://github.com/akmalsoliev)
