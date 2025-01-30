from __future__ import annotations

from typing import Callable, Union

import modin.pandas as mpd
import pandas as pd
import polars as pl
import pyarrow as pa
import pytest
from _pytest.fixtures import SubRequest
from narwhals import generate_temporary_column_name
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import lit

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


def spark_df(data: dict[str, list]) -> DataFrame:
    session = (
        SparkSession.builder.appName("DataFrameCreation")
        .master("local[*]")
        .config("spark.driver.memory", "1g")
        .getOrCreate()
    )
    index_col_name = generate_temporary_column_name(n_bytes=8, columns=list(data))
    data[index_col_name] = list(range(len(data[next(iter(data))])))

    null_cols = [key for key, values in data.items() if all(v is None for v in values)]
    for key in null_cols:
        del data[key]

    sp_df = (  # type: ignore[no-any-return]
        session.createDataFrame([*zip(*data.values())], schema=[*data.keys()])
        .repartition(2)
        .orderBy(index_col_name)
        .drop(index_col_name)
    )
    for col in null_cols:
        sp_df = sp_df.withColumn(col, lit(None))

    return sp_df


def create_frame_fixture(func: Callable) -> Callable:
    @pytest.fixture(
        params=[
            ("pandas", pandas_df),
            ("polars_df", polars_df),
            ("polars_lf", polars_lf),
            ("pyarrow_array", pyarrow_array),
            ("pyspark", spark_df),
        ],
        ids=["pandas", "polars_df", "polars_lf", "pyarrow_array", "pyspark"],
    )
    def wrapper(request: SubRequest) -> ReturnType:
        _, df_factory = request.param
        data = func()
        return df_factory(data)

    return wrapper
