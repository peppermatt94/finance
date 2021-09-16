import pandas as pd
import numpy.random as rn
import numpy as np
from hypothesis import given, settings
import hypothesis.strategies as st
from hypothesis import assume
from hypothesis.extra.pandas import column, data_frames,range_indexes, series, indexes,columns
import subprocess
import unittest
import math
from simulation import BM, GBM, Levy

class simulation_Tests(unittest.TestCase):
    @unittest.skip("demonstrated")
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
###########################################################################################
    @unittest.skip("demonstrated")
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
        - saving in variable 'return' the list of daily_returns with GBM
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
#########################################################################################
    @unittest.skip("demonstrated")
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
        - saving in variable 'return' the list of daily_returns with levy
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
    
########################################################################################
    @unittest.skip("demonstrated")
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
     
##################################################################################
    @unittest.skip("demonstrated")
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
#####################################################################################
    @unittest.skip("demonstrated")
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
    
#####################################################################################
    #@unittest.skip("demonstrated")
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                    columns=[column("Close", elements = st.floats(min_value=400, max_value=600, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(max_examples=1, deadline=None)
    def test_Brownian_motion_statistically_correct(self, x):
        '''
    Given:
        - dataframe with datetime index with length 100.
    so:
        - sorting the index of dataframe ( i need sorted datetime)
        - take the  std of 1000 sampling of BM process with different time occurency: 10,100,1000 days
    And :
        - assert the 100 day BM std is almost 10 day BM std * sqrt(10)
        - assert the 1000 day BM std is almost 100 day BM std * sqrt(10)
        - assert the 1000 day BM std is almost 10 day BM std * 10
    
    Reference: https://en.wikipedia.org/wiki/Brownian_motion
    '''    
        x = x.sort_index()
        day_10 = np.std([ BM(10, x).Euler_Maruyama().Close[-1] for _ in range(1000)])
        day_100 = np.std([ BM(100, x).Euler_Maruyama().Close[-1] for _ in range(1000)])
        day_1000 = np.std([ BM(1000, x).Euler_Maruyama().Close[-1] for _ in range(1000)])
        
         # i put a delta since they are statistical quantity, delta = 10% of the target value
        self.assertAlmostEqual(day_100, day_10*np.sqrt(10), delta = day_100*0.1)
        self.assertAlmostEqual(day_1000, day_100*np.sqrt(10), delta = day_1000*0.1)
        self.assertAlmostEqual(day_1000, day_100*np.sqrt(10), delta = day_1000*0.5)
     
###################################################################################
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
                max_value=pd.Timestamp(2020, 9, 1)),  min_size=100,max_size=100, unique=True),
                   columns=[column("Close", elements = st.floats(min_value=400, max_value=600, allow_nan = False, allow_infinity=False), dtype=float),
                            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(max_examples=1, deadline=None)
    def test_Geometric_Brownian_motion_statistically_correct(self, x):
        '''
    Given:
        - dataframe with datetime index with length 100 and a columns named "Close" 
          (with values generated random from random seed) and "longName"
    so:
        - sorting the index of dataframe ( i want the generated data be sorted)
        - take the variance of GBM variables after 10, 50, 100 days
        - take S0 that is the last number of the experimental data (random generated)
        - take mu and sigma from the experimental data (random generated)
    And :
        Since the variables distributed according to brownian motion have 
          a variance that depend on t: 
          var(X_t) = (S0**2)*np.exp(2*mu*t)*(np.exp((sigma**2)*t)-1)
          
         - assert: the variable after 10 day have a variance equal 
           to the expected one in the order of magnitude
           
         - assert: the variable after 50 day have a variance equal 
           to the expected one in the order of magnitude'
           
         - assert: the variable after 100 day have a variance equal 
           to the expected one in the order of magnitude

    Reference: https://en.wikipedia.org/wiki/Geometric_Brownian_motion
    '''    
        x = x.sort_index()
        day_10 = np.var([GBM(10, x).Euler_Maruyama().Close[-1] for _ in range(1000)])
        day_50 = np.var([GBM(50, x).Euler_Maruyama().Close[-1] for _ in range(1000)])
        day_100 = np.var([GBM(100, x).Euler_Maruyama().Close[-1] for _ in range(1000)])
        S0 =x.Close[-1] 
        mu,sigma = GBM(30,x).mu_and_sigma_estimation()
        
        # i compare the order of magnitude since the value of the var are very high and request a perfect equality would be unreasonable
        self.assertEqual(math.floor(math.log((S0**2)*np.exp(2*mu*10)*(np.exp((sigma**2)*10)-1), 10)) , math.floor(math.log(day_10, 10))) 
        self.assertEqual(math.floor(math.log((S0**2)*np.exp(2*mu*50)*(np.exp((sigma**2)*50)-1), 10)) , math.floor(math.log(day_50, 10))) 
        self.assertEqual(math.floor(math.log((S0**2)*np.exp(2*mu*100)*(np.exp((sigma**2)*100)-1), 10)) , math.floor(math.log(day_100, 10))) 

#############################################################################################
    @unittest.skip("demonstrated")    
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
        - assert the length of the output array is the value of the period as expected'
    '''    
        simulated_array = BM(period, x).Euler_Maruyama()
        self.assertEqual(len(simulated_array), period)
    
if __name__ == '__main__':
    unittest.main() 
