from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import TYPE_CHECKING, Callable, cast

import narwhals as nw
from loguru import logger
from narwhals.typing import IntoFrame

from validoopsie.base.results_typedict import (
    ResultValidationTypedDict,
    SummaryTypedDict,
    ValidationTypedDict,
)

if TYPE_CHECKING:
    from validoopsie.base import BaseValidation


class Validate:
    def __into_narwhalsframe__(self, frame: IntoFrame) -> IntoFrame:
        """Convert a native frame to a narwhals frame."""
        return nw.from_native(frame)

    def __init__(self, frame: IntoFrame) -> None:
        self.summary = SummaryTypedDict(
            passed=None,
            validations=[],
            failed_validation=[],
        )

        self.results: dict[str, SummaryTypedDict | ValidationTypedDict] = {
            "Summary": self.summary,
        }

        self.frame: IntoFrame = self.__into_narwhalsframe__(frame)
        self.__generate_validation_attributes__()

    def __generate_validation_attributes__(self) -> None:
        validoopsie_dir = Path(__file__).parent
        oops_catalogue_dir = validoopsie_dir / "validation_catalogue"

        # Get list of subdirectories in validation_catalogue
        subdirectories = [d for d in oops_catalogue_dir.iterdir() if d.is_dir()]

        for subdir in subdirectories:
            subclass_name = subdir.name
            subclass = type(subclass_name, (), {})
            subclass.__doc__ = f"Validation checks for {subclass_name}"

            # List of Python files in the subdirectory, excluding __init__.py
            py_files = [f for f in subdir.glob("*.py") if f.name != "__init__.py"]

            for py_file in py_files:
                # Get module name including package
                module_relative_path = py_file.relative_to(validoopsie_dir.parent)
                module_name = ".".join(module_relative_path.with_suffix("").parts)

                module = importlib.import_module(module_name)
                module_keys = module.__dict__.keys()

                for key in module_keys:
                    if py_file.stem.replace("_", "").lower() in key.lower():
                        try:
                            func: type = module.__dict__[key]
                            setattr(
                                subclass,
                                key,
                                self.__make_validation_method__(func),
                            )

                        except KeyError:
                            msg = f"Could not load module {module_name} from {py_file}"
                            logger.warning(msg)
                        except ImportError:
                            msg = f"Could not load module {module_name} from {py_file}"
                            logger.warning(msg)

                        break

            # Attach the subclass to the Validate instance
            setattr(self, subclass_name, subclass())

    def __make_validation_method__(
        self,
        class_obj: type,
    ) -> Callable[..., Validate]:
        def validation_method(*args, **kwargs) -> Validate:
            return self.__create_validation_class__(
                class_obj,
                *args,
                **kwargs,
            )

        validation_method.__name__ = class_obj.__name__
        validation_method.__doc__ = class_obj.__doc__

        return validation_method

    def __create_validation_class__(
        self,
        validation_class: type,
        *args: list[object],
        **kwargs: dict[str, object],
    ) -> Validate:
        args = args[1:]
        validation = validation_class(*args, **kwargs)
        result: ValidationTypedDict = validation.__execute_check__(frame=self.frame)
        name: str = f"{validation.__class__.__name__}_{validation.column}"
        self.__parse_results__(name, result)
        return self

    def __parse_results__(self, name: str, result_dict: ValidationTypedDict) -> None:
        status: str = result_dict["result"]["status"]
        # If the validation check failed, set the overall result to Fail
        # If No validations are added, the result will be None
        # If all validations pass, the result will be Success
        if status == "Fail":
            self.summary["passed"] = False
            if "failed_validation" not in self.summary:
                self.summary["failed_validation"] = [name]
            else:
                self.summary["failed_validation"].append(name)
        elif self.summary["passed"] is None and status == "Success":
            self.summary["passed"] = True

        if isinstance(self.summary["validations"], str):
            self.summary["validations"] = [name]
        else:
            self.summary["validations"].append(name)

        # appending the results to the list of all validations
        self.results[name] = result_dict

    def add_validation(
        self,
        validation: BaseValidation,
    ) -> Validate:
        """Add custom generated validation check to the Validate class instance.

        Args:
            validation (BaseValidationParameters): Custom validation check to add

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> from validoopsie import Validate
            >>> from validoopsie.base import BaseValidation
            >>>
            >>> # Create a custom validation class
            >>> class CustomValidation(BaseValidation):
            ...     def __init__(self, column, impact="low", threshold=0.0, **kwargs):
            ...         super().__init__(column, impact, threshold, **kwargs)
            ...
            ...     @property
            ...     def fail_message(self) -> str:
            ...         return f"Custom validation failed for column {self.column}"
            ...
            ...     def __call__(self, frame):
            ...         # Custom validation logic
            ...         return (
            ...             # Note: that select `None` for an empty DataFrame
            ...             frame.select(nw.all() == None)
            ...             .group_by(self.column)
            ...             .agg(nw.col("column1").sum().alias("column1-count"))
            ...         )
            ...
            >>> # Apply custom validation
            >>> df = pd.DataFrame({"column1": [1, 2, 3]})
            >>>
            >>> vd = (
            ...     Validate(df)
            ...     .add_validation(CustomValidation(column="column1"))
            ... )
            >>> key = "CustomValidation_column1"
            >>> vd.results[key]["result"]["status"]
            'Success'
            >>>
            >>> # When calling validate on successful validation there is no error.
            >>> vd.validate()

        """
        output_name: str = "InvalidValidationCheck"
        result: ValidationTypedDict
        output: ResultValidationTypedDict

        try:
            from validoopsie.base.base_validation import (  # noqa: PLC0415
                BaseValidation,
            )

            assert isinstance(validation, BaseValidation)
        # This is under the condition that the validation is not of type BaseValidation
        except AssertionError:
            # Get class name safely
            output_name = (
                getattr(validation, "__name__", str(validation))
                if inspect.isclass(validation)
                else type(validation).__name__
            )
            output = ResultValidationTypedDict(
                status="Fail",
                message=f"{output_name} is not a valid validation check.",
            )

            result = ValidationTypedDict(
                validation=output_name,
                impact="high",
                timestamp="N/A",
                column="N/A",
                result=output,
            )

            self.__parse_results__(output_name, result)
            return self

        class_name = validation.__class__.__name__
        try:
            result = validation.__execute_check__(frame=self.frame)
            column_name = validation.column
            output_name = f"{class_name}_{column_name}"
        except Exception as e:
            output = ResultValidationTypedDict(
                status="Fail",
                message=(f"An error occured while executing {class_name} - {e!s}"),
            )
            result = ValidationTypedDict(
                validation=output_name,
                impact="high",
                timestamp="N/A",
                column="N/A",
                result=output,
            )

        self.__parse_results__(output_name, result)
        return self

    def validate(self, *, raise_results: bool = False) -> None:
        """Validate the dataset by running all configured validation checks.

        This method processes all validation results stored in `self.results` and handles
        them based on their impact level. It logs validation outcomes and optionally
        raises exceptions for failed high-impact validations.

        Args:
            raise_results: If True, includes detailed validation results in the exception
                message when high-impact validations fail. If False, only includes the
                names of failed validations. Defaults to False.

        Raises:
            ValueError: If no validation checks were added (only "Summary" key exists
                in results), or if any high-impact validation checks fail.

        Logging Behavior:
            - High-impact failures: Logged at CRITICAL level
            - Medium-impact failures: Logged at ERROR level
            - Low-impact failures: Logged at WARNING level
            - Successful validations: Logged at INFO level

        Impact Level Handling:
            - **High impact**: Failures cause ValueError to be raised
            - **Medium impact**: Failures are logged as errors but don't raise exceptions
            - **Low impact**: Failures are logged as warnings but don't raise exceptions

        Note:
            The "Summary" key in results is automatically skipped as it contains
            aggregate information rather than individual validation check results.

        Example:
            .. code-block:: python
            validator.validate()  # Raises ValueError if high-impact checks fail
            validator.validate(raise_results=True)  # Includes detailed results error
        """
        if len(self.summary["validations"]) == 0:
            msg = "No validation checks were added."
            raise ValueError(msg)

        list_of_failed_validations_string: list[str] = []
        for name in self.results:
            # Skip the overall result, as it is not a validation check
            if name == "Summary":
                continue

            validation: ValidationTypedDict = cast(
                "ValidationTypedDict", self.results[name]
            )

            assert "validation" in validation

            impact = validation.get("impact", "high").lower()

            # Check if the validation failed and if it is high impact then it
            # should raise an error
            failed = validation["result"]["status"] == "Fail"

            if failed:
                message = validation["result"]["message"]
                warning_msg = f"Failed validation: {name} - {message}"
                if impact == "high":
                    list_of_failed_validations_string.append(name)
                    logger.critical(warning_msg)
                elif impact == "medium":
                    logger.error(warning_msg)
                elif impact == "low":
                    logger.warning(warning_msg)
                else:
                    msg = "impact is not set, this is an error please open an issue"
                    raise KeyError(msg)
            else:
                info_msg = f"Passed validation: {validation}"
                logger.info(info_msg)

        if list_of_failed_validations_string:
            value_error_msg = f"Failed Validation(s): {list_of_failed_validations_string}"

            if raise_results:
                import json  # noqa: PLC0415

                json_results = json.dumps(self.results, indent=4)
                value_error_msg = f"{value_error_msg}\n{json_results}"

            raise ValueError(value_error_msg)
