import narwhals as nw
import pytest
from narwhals.typing import FrameT, IntoFrame

from tests.utils.create_frames import create_frame_fixture
from validoopsie import Validate
from validoopsie.base import BaseValidation


@create_frame_fixture
def sample_data() -> dict[str, list]:
    return {
        "date": ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01"],
        "temperature": [50, 60, 70, 80],
    }


class MyCustomValidation(BaseValidation):
    def __init__(
        self,
        column: str,
        *args,
        **kwargs: dict[str, object],
    ) -> None:
        super().__init__(column, *args, **kwargs)

    @property
    def fail_message(self) -> str:
        """Return the fail message used in the report."""
        return (
            # This is very flexible and we can just add a custom message that would like
            # to be used.
            "My new custom validation failed!"
        )

    def __call__(self, frame: FrameT) -> FrameT:
        """My new custom validation.

        The result will be used during execution.
        """
        return (
            frame.group_by(self.column)
            .agg(nw.col("temperature").mean().alias("mean_temperature_farenheit"))
            .with_columns(
                ((nw.col("mean_temperature_farenheit") - 35) * 5 / 9).alias(
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


def test_adding_custom_validation(sample_data: IntoFrame) -> None:
    column_name = "date"
    validation_name = f"{MyCustomValidation.__name__}_{column_name}"

    vd = Validate(sample_data)
    vd.add_validation(MyCustomValidation("date"))
    results = vd.results

    assert results[validation_name]["result"]["status"] == "Success"
    vd.validate()


class FailValidation: ...


def test_adding_failed_validation(sample_data: IntoFrame) -> None:
    validation_name = FailValidation.__name__

    vd = Validate(sample_data)
    vd.add_validation(FailValidation)
    results = vd.results

    assert results[validation_name]["result"]["status"] == "Fail"

    with pytest.raises(ValueError):
        vd.validate()
