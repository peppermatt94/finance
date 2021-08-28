import pandas as pd
import numpy.random as rn
import numpy as np
from hypothesis import given, settings
import hypothesis.strategies as st
from hypothesis import assume
from hypothesis.extra.pandas import column, data_frames,range_indexes, series, indexes,columns
import subprocess
import unittest

from simulation import BM

class simulation_Tests(unittest.TestCase):
    @given(x = data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats( allow_nan = True, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_drop_nan(self,x):
        x = x.sort_index()
        x[x.Close<0.1] = 0.1   # i put some upper and lower limit on the data created
        x[x.Close>1000] = 1000
        returns = BM(100,x).daily_return()
        count = 0
        for daily in returns:
            if daily == np.nan:
                count+=1                
        self.assertEqual(count, 0)
    
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_all_equal_values_give_null_vol(self, x):
        x = x.sort_index()
        x.to_csv("simulation.csv")
        mu, sigma = BM(100, x).mu_and_sigma_estimation()
        self.assertEqual( sigma, 0)

        
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_all_equal_values_give_same_mu(self, x):
        x = x.sort_index()
        x.to_csv("simulation.csv")
        mu, sigma = BM(100, x).mu_and_sigma_estimation()
        self.assertEqual( mu, 0)  
   
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_normal_distributed_data_give_correct_mu(self, x):
        normal_distribution = rn.normal(0, 10, 100)
        x.Close = normal_distribution
        mu, sigma = BM(100, x).mu_and_sigma_estimation()
        self.assertAlmostEqual(mu, 0, delta = 5) 
          
    @given(x = data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]), 
           period = st.integers(min_value=10, max_value= 500))
    @settings(deadline=None)    
    def test_euler_maruyama_yelds_correct_period(self, x, period):
        simulated_array = BM(period, x).Euler_Maruyama()
        self.assertEqual(len(simulated_array), period)
    
if __name__ == '__main__':
    unittest.main() 
