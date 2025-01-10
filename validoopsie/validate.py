from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import narwhals as nw
from loguru import logger
from narwhals.typing import Frame, IntoFrame

if TYPE_CHECKING:
    from validoopsie.base.base_validation_parameters import BaseValidationParameters
    from validoopsie.types import KwargsType


class Validate:
    def __into_narwahlframe__(self, frame: IntoFrame) -> Frame:
        """Convert a native frame to a narwhals frame."""
        return nw.from_native(frame)

    def __init__(self, frame: IntoFrame) -> None:
        self.results = {
            "Summary": {
                "passed": None,
                "validations": "No validation checks were added.",
            },
        }
        self.frame: Frame = self.__into_narwahlframe__(frame)
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

                # Import the module from the file path
                spec = importlib.util.spec_from_file_location(
                    module_name,
                    py_file,
                )
                module = importlib.util.module_from_spec(spec)
                if spec.loader:
                    spec.loader.exec_module(module)
                else:
                    msg = f"Could not load module {module_name} from {py_file}"
                    logger.warning(msg)
                    continue

                file_name_lower = py_file.stem.replace("_", "").lower()
                # Find classes defined in the module
                classes_in_module = inspect.getmembers(
                    module,
                    lambda member: inspect.isclass(member)
                    and member.__name__.lower() == file_name_lower,
                )

                for _, class_obj in classes_in_module:
                    # Attach the method to the subclass
                    setattr(
                        subclass,
                        class_obj.__name__,
                        self.__make_validation_method__(class_obj),
                    )

            # Attach the subclass to the DataSet instance
            setattr(self, subclass_name, subclass())

    def __make_validation_method__(self, class_obj: type) -> Callable[..., Validate]:
        def validation_method(*args, **kwargs) -> Validate:
            return self.__create_validation_class__(
                class_obj,
                *args,
                **kwargs,
            )

        validation_method.__name__ = class_obj.__name__
        validation_method.__doc__ = class_obj.__doc__

        return validation_method

    def __parse_results__(self, result: dict, name: str) -> None:
        status = result["result"]["status"]
        # If the validation check failed, set the overall result to fail
        # If No validations are added, the result will be None
        # If all validations pass, the result will be PASS
        if status == "Fail":
            self.results["Summary"]["passed"] = False
            if "Failed Validation" not in self.results["Summary"]:
                self.results["Summary"]["Failed Validation"] = [name]
            else:
                self.results["Summary"]["Failed Validation"].append(name)
        elif self.results["Summary"]["passed"] is None and status == "Success":
            self.results["Summary"]["passed"] = True

        if isinstance(self.results["Summary"]["validations"], str):
            self.results["Summary"]["validations"] = [name]
        else:
            self.results["Summary"]["validations"].append(name)

        self.results.update({name: result})

    def __create_validation_class__(
        self,
        validation_class: type,
        *args: str | list[str | int] | int,
        **kwargs: KwargsType,
    ) -> Validate:
        args = args[1:]
        validation = validation_class(*args, **kwargs)
        result = validation.__execute_check__(frame=self.frame)
        name = f"{validation.__class__.__name__}_{validation.column}"
        self.__parse_results__(result, name)
        return self

    def add_validation(
        self,
        validation: BaseValidationParameters,
    ) -> Validate:
        """Add custom generated validation check to the Validate class instance.

        Args:
            validation (type): Custom generated validation check

        """
        output_name: str = "InvalidValidationCheck"
        if hasattr(validation, "__execute_check__"):
            class_name = validation.__class__.__name__
            try:
                result = validation.__execute_check__(frame=self.frame)
                column_name = validation.column
                output_name = f"{class_name}_{column_name}"
            except Exception as e:
                result = {
                    "result": {
                        "status": "Fail",
                        "message": f"An error occured while executing {class_name} - {e!s}",
                    },
                }
        else:
            result = {
                "result": {
                    "status": "Fail",
                    "message": f"{validation.__name__} is not a valid validation check.",
                },
            }
            if inspect.isclass(validation):
                output_name = validation.__name__

        self.__parse_results__(result, output_name)
        return self

    def validate(self) -> Validate:
        """Validate the data set."""
        if self.results.keys().__len__() == 1:
            msg = "No validation checks were added."
            raise ValueError(msg)
        failed_validations: list[str] = []
        for key in self.results:
            # Skip the overall result, as it is not a validation check
            if key == "Summary":
                continue

            impact = self.results[key].get("impact", "high")

            # Check if the validation failed and if it is high impact then it
            # should raise an error
            failed = self.results[key]["result"]["status"] == "Fail"
            high_impact = impact.lower() == "high"
            medium_impact = impact.lower() == "medium"

            if failed and high_impact:
                failed_validations.append(key)
                warning_msg = (
                    f"Failed validation: {key} - {self.results[key]['result']['message']}"
                )
                logger.critical(warning_msg)
            elif failed and medium_impact:
                warning_msg = (
                    f"Failed validation: {key} - {self.results[key]['result']['message']}"
                )
                logger.warning(warning_msg)
            elif failed:
                warning_msg = (
                    f"Failed validation: {key} - {self.results[key]['result']['message']}"
                )
                logger.error(warning_msg)
            else:
                info_msg = f"Passed validation: {key}"
                logger.info(info_msg)
        if failed_validations:
            value_error_msg = f"FAILED VALIDATION(S): {failed_validations}"
            raise SystemExit(value_error_msg)
        return self
