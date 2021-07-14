# -*- coding: utf-8 -*-
import pandas as pd
from hypothesis import given, settings
import hypothesis.strategies as st
from hypothesis import assume
from hypothesis.extra.pandas import column, data_frames,range_indexes, series, indexes,columns

def test_if_the_ticker_is_not_in_listOfCompany():
    pass


@given( data_frames(index=indexes(st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False), dtype=float)]))
@settings(deadline=None)
def test_volatility_estimation_give_correct_result(x):
    import DataAnalyzers as Da
    assert Da.volatility_estimation(x) == 0.0
     
data = data_frames(index=indexes(st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False), dtype=float)])