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
2. Install the required dependencies (I prefer using `uv` for this):
    ```sh
    uv sync --all-extras
    ```

## Running Tests

We use `pytest` for running tests. To run the tests, execute the following command:
```sh
pytest
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
