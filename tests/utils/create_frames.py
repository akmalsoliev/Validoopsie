from __future__ import annotations

from typing import Callable, Union

import modin.pandas as mpd
import pandas as pd
import polars as pl
import pyarrow as pa
import pytest
from _pytest.fixtures import SubRequest

ReturnType = Union[pl.DataFrame, pd.DataFrame, pl.LazyFrame, pa.Table]


def polars_lf(data: dict[str, list]) -> pl.DataFrame:
    return pl.DataFrame(data)


def polars_df(data: dict[str, list]) -> pl.DataFrame:
    return pl.DataFrame(data)


def pandas_df(data: dict[str, list]) -> pd.DataFrame:
    return pd.DataFrame(data)


def pyarrow_array(data: dict[str, list]) -> pa.Table:
    return pa.Table.from_pydict(data)


def modin_df(data: dict[str, list]) -> mpd.DataFrame:
    return mpd.DataFrame(data)


def create_frame_fixture(func: Callable) -> Callable:
    @pytest.fixture(
        params=[
            ("pandas", pandas_df),
            ("polars_df", polars_df),
            ("polars_lf", polars_lf),
            ("pyarrow_array", pyarrow_array),
        ],
        ids=["pandas", "polars_df", "polars_lf", "pyarrow_array"],
    )
    def wrapper(request: SubRequest) -> ReturnType:
        _, df_factory = request.param
        data = func()
        return df_factory(data)

    return wrapper
