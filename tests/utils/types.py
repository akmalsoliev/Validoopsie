from typing import Union

import modin.pandas as mpd
import pandas as pd
import polars as pl
import pyarrow as pa

ReturnT = Union[pl.DataFrame, pd.DataFrame, pl.LazyFrame, pa.Table, mpd.DataFrame]
