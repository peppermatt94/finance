import pandas as pd
import numpy.random as rn
import numpy as np
from hypothesis import given, settings
import hypothesis.strategies as st
from hypothesis import assume
from hypothesis.extra.pandas import column, data_frames,range_indexes, series, indexes,columns
import subprocess
import unittest

from simulation import BM, GBM, Levy

class simulation_Tests(unittest.TestCase):
    #@unittest.skip("demonstrated")
    @given(x = data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats( allow_nan = True, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_drop_nan_BM(self,x):
        '''
    Given:
        - Dataframe with datetime index and columns named "Close" and "longName".
    So:
        - sorting the dataframe respect to date
        - imposing upper and lower limit to avoid random generation of too big or too small values 
        - saving in variable 'return' the list of daily_returns
    And :
        - assert the number of nan in list (count) is zero (nan suppression)'
        '''    
        x = x.sort_index()
        x[x.Close<0.1] = 0.1   # i put some upper and lower limit on the data created
        x[x.Close>1000] = 1000
        returns = BM(100,x).daily_return()
        count = 0
        for daily in returns:
            if daily == np.nan:
                count+=1                
        self.assertEqual(count, 0)
        
    #@unittest.skip("demonstrated")
    @given(x = data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats( allow_nan = True, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_drop_nan_GBM(self,x):
        '''
    Given:
        - Dataframe with datetime index and columns named "Close" and "longName".
    So:
        - sorting the dataframe respect to date
        - imposing upper and lower limit to avoid random generation of too big or too small values 
        - saving in variable 'return' the list of daily_returns
    And :
        - assert the number of nan in list (count) is zero (nan suppression)'
        '''    
        x = x.sort_index()
        x[x.Close<0.1] = 0.1   # i put some upper and lower limit on the data created
        x[x.Close>1000] = 1000
        returns = GBM(100,x).daily_return()
        count = 0
        for daily in returns:
            if daily == np.nan:
                count+=1                
        self.assertEqual(count, 0)
        
    #@unittest.skip("demonstrated")
    @given(x = data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
                   columns=[column("Close", elements = st.floats( allow_nan = True, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_drop_nan_levy(self,x):
        '''
    Given:
        - Dataframe with datetime index and columns named "Close" and "longName".
    So:
        - sorting the dataframe respect to date
        - imposing upper and lower limit to avoid random generation of too big or too small values 
        - saving in variable 'return' the list of daily_returns
    And :
        - assert the number of nan in list (count) is zero (nan suppression)'
        '''    
        x = x.sort_index()
        x[x.Close<0.1] = 0.1   # i put some upper and lower limit on the data created
        x[x.Close>1000] = 1000
        returns = Levy(100,x).daily_return()
        count = 0
        for daily in returns:
            if daily == np.nan:
                count+=1                
        self.assertEqual(count, 0)
    
    
    #@unittest.skip("demonstrated")
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_normal_distributed_data_give_correct_mu_BM(self, x):
        '''
    Given:
        - Dataframe with datetime index and columns named "Close" and "longName" with all equal values
    so:
        - creating a normal distributed array and put it in "Close" column with zero mean
        - sorting index
        - compute mu with BM
    And :
        - assert mu is zero as expected '
    '''    
        normal_distribution = rn.normal(0, 10, 100)
        x.Close = normal_distribution
        mu, sigma = BM(100, x).mu_and_sigma_estimation()
        self.assertAlmostEqual(mu, 0, delta = 5)
     
    #@unittest.skip("demonstrated")
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_normal_distributed_data_give_correct_mu_GBM(self, x):
        '''
    Given:
        - Dataframe with datetime index and columns named "Close" and "longName" with all equal values
    so:
        - creating a normal distributed array and put it in "Close" column with zero mean
        - sorting index
        - compute mu with GBM
    And :
        - assert mu is zero as expected '
    '''    
        normal_distribution = rn.normal(0, 10, 100)
        x.Close = normal_distribution
        mu, sigma = GBM(100, x).mu_and_sigma_estimation()
        self.assertAlmostEqual(mu, 0, delta = 5)
        
    #@unittest.skip("demonstrated")
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_normal_distributed_data_give_correct_mu_levy(self, x):
        '''
    Given:
        - Dataframe with datetime index and columns named "Close" and "longName" with all equal values
    so:
        - creating a normal distributed array and put it in "Close" column with zero mean
        - sorting index
        - compute mu with levy
    And :
        - assert mu is zero as expected '
    '''    
        normal_distribution = rn.normal(0, 10, 100)
        x.Close = normal_distribution
        mu, sigma = Levy(100, x).mu_and_sigma_estimation()
        self.assertAlmostEqual(mu, 0, delta = 5)
    
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                    columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(max_examples=1, deadline=None)
    def test_Brownian_motion_statistically_correct(self, x):
        '''
    Given:
        - dataframe with datetime index with length 100.
    so:
        - sorting the index of dataframe
        - fullfilling the 'Close' column with random normal data with casual seed
        - construct a list of std of the BM simulation with differents length with a loop
           for three different periods of simulation
        - take  the mean of the list associated to  each period of simulation
    And :
        - assert the geometric brownian motion increase the std increasing the time step with sqrt(t)'
    Reference: https://en.wikipedia.org/wiki/Brownian_motion
    '''    
        normal_distribution =  rn.normal(50,0.1,100)  # i train the simulation with a random numbers created with random seed
        x = x.sort_index()
        x.Close = normal_distribution
        day_10 = []
        day_100 = []
        day_1000 = []
        for i in range(1000):
            day_10.append(np.std( BM(10, x).Euler_Maruyama().Close))
            day_100.append(np.std( BM(100, x).Euler_Maruyama().Close))
            day_1000.append(np.std( BM(1000, x).Euler_Maruyama().Close))
        
        day_10std = np.mean(day_10)
        day_100std = np.mean(day_100)
        day_1000std = np.mean(day_1000)
        
         # i put a delta since they are statistical quantity, delta = 1 is small
        self.assertAlmostEqual(day_100std, day_10std*np.sqrt(10), delta = 1)
        self.assertAlmostEqual(day_1000std, day_100std*np.sqrt(10), delta = 1)
        
     
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(max_examples=1, deadline=None)
    def test_Geometric_Brownian_motion_statistically_correct(self, x):
        '''
    Given:
        - dataframe with datetime index with length 100 and a columns named "Close" and "longName"
    so:
        - sorting the index of dataframe
        - fullfilling the 'Close' column with random normal data with casual seed
        - construct a list of std of the GBM simulation with differents length with a loop
           for three different periods of simulation
        - take the mean of the list associated to each period of simulation
    And :
        - assert the brownian motion increase the std with increasing the time step by a factor sqrt(t)'
    Reference: https://en.wikipedia.org/wiki/Geometric_Brownian_motion
    '''    
        normal_distribution = rn.normal(50,0.1,100) # i train the simulation with a random numbers created with random seed
        x = x.sort_index()
        x.Close = normal_distribution
        day_10 = []
        day_100 = []
        day_1000 = []
        for i in range(1000): # i want to create statistacal limit for variance
            day_10.append(np.var( GBM(10, x).Euler_Maruyama().Close))
            day_100.append(np.var( GBM(100, x).Euler_Maruyama().Close))
            day_1000.append(np.var( GBM(1000, x).Euler_Maruyama().Close))

        day_10std = np.mean(day_10)
        day_100std = np.mean(day_100)
        day_1000std = np.mean(day_1000)
        
        # i put a delta since they are statistical quantity, small delta chosen
        self.assertAlmostEqual(day_100std, day_10std*10, delta = 0.1) 
        self.assertAlmostEqual(day_1000std, day_100std*10, delta = 1)    
    
    
    #@unittest.skip("demonstrated")    
    @given(x = data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=500, max_value=500, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]), 
           period = st.integers(min_value=10, max_value= 500))
    @settings(deadline=None)    
    def test_euler_maruyama_yelds_correct_period(self, x, period):
        '''
    Given:
        - dataframe with datetime index and column named 'Close' and 'longName'.
        - random period of simulation
    so:
        - create a BM simulation in simulated_array
    And :
        - assert the length of the output array is the value of the period'
    '''    
        simulated_array = BM(period, x).Euler_Maruyama()
        self.assertEqual(len(simulated_array), period)
    
if __name__ == '__main__':
    unittest.main() 
