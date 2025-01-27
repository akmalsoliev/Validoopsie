# Contribution Guidelines

Thank you for considering contributing to Validoopsie! The idea of one spending their time
on contribution to this project is wild for me, so I appreciate every minute you spend on it.

## How to Contribute

1. Fork the repository on GitHub and clone your fork to your local machine:
    ```sh
    git clone https://github.com/your-username/Validoopsie.git
    ```
1. Install the required dependencies (I prefer using `uv` for this):
    ```sh
    uv sync --all-extras
    ```
If you want to modify the documentation, you will also need to install the documentation dependencies:
    ```sh
    uv sync --group docs
    ```

2. Create a new branch for your feature or bugfix:
    ```sh
    git checkout -b my-feature-branch
    ```
3. Make your changes in the new branch.
4. Run the tests to ensure that your changes do not break anything:
    ```sh
    pytest
    ```
5. Commit your changes with a descriptive commit message:
    ```sh
    git commit -m "Add feature X"
    ```
6. Push your branch to your fork on GitHub:
    ```sh
    git push origin my-feature-branch
    ```
7. Open a pull request on the main repository.

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
