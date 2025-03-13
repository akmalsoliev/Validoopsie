# Contribution Guidelines

Thank you for considering contributing to Validoopsie! The idea of one spending their time
on contribution to this project is wild for me, so I appreciate every minute you spend on it.

## Table of Contents

1. [How to Contribute](#how-to-contribute)
2. [Setting Up the Development Environment](#setting-up-the-development-environment)
3. [Running Tests](#running-tests)
4. [Submitting Changes](#submitting-changes)
5. [Style Guide](#style-guide)


## How to Contribute

1. Fork the repository on GitHub.
2. Clone your fork to your local machine:
    ```sh
    git clone https://github.com/your-username/Validoopsie.git
    ```
3. Create a new branch for your feature or bugfix:
    ```sh
    git checkout -b my-feature-branch
    ```
4. Make your changes in the new branch.
5. Run the tests to ensure that your changes do not break anything:
    ```sh
    pytest
    ```
6. Commit your changes with a descriptive commit message:
    ```sh
    git commit -m "Add feature X"
    ```
7. Push your branch to your fork on GitHub:
    ```sh
    git push origin my-feature-branch
    ```
8. Open a pull request on the main repository.

## Setting Up the Development Environment

1. Ensure you have Python 3.9 or higher installed.
2. Use the Makefile to set up the development environment:
    ```sh
    make setup
    ```
   
   This will create a virtual environment and install all dependencies.

   Alternatively, you can install dependencies manually:
    ```sh
    uv sync --all-extras
    ```

## Running Tests and Linters

We use a Makefile to simplify development tasks:

```sh
# Run linters (mypy, ruff)
make lint

# Run tests (includes doctests, stubtest)
make test

# Run both lint and test
make all
```

You can also run specific commands directly:
```sh
# Run pytest
pytest

# Run mypy type checking
mypy validoopsie/

# Run ruff linter
ruff check validoopsie/
```


## Submitting Changes

1. Ensure that your code follows the project's Style-guide (basically ruff).
2. Ensure that all tests pass.
3. Open a pull request with a clear title and description of your changes.
4. Be prepared to make changes requested by reviewers.

## Style Guide

- Follow the PEP 8 style guide for Python code.
- Use type hints where appropriate.
- Ensure that your code is well-documented.
- Use meaningful variable and function names.

Thank you for your contributions!
