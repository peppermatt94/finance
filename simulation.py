import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from datetime import datetime
from numpy import random as rd
from tqdm import tqdm

def Euler_Maruyama(a,b,x0,data_of_simulation_period_void):    #Integration of the black scholes equation: ITO process
    '''Integration of the ITO process. Here i use euler-maruyama approximation
    
        Parameters
        ----------
        a : callable
            The interest rate respect time a(x_t,t), x_t is vector position
        b : callable
            the volatility  respect time b(x,t), x_t is vector
        x0: float 
            starting value
        data_of_simulation_period_void: pandas dataframe to fullfill with new data, the index must be
            already estabilished as datetime index that coincide with the period 
            to simulate. The column "Close" can be fullfilled with fictious data to
            override (or zeros)            
            
        Returns
        -------
        data_of_simulation_period filled, by the ITO simulation
        
        References
        https://jtsulliv.github.io/stock-movement/
        https://en.wikipedia.org/wiki/Euler%E2%80%93Maruyama_method
        '''
    #I start to fullfilled data_of_simulation_period_void with the correct data:
    #I use two tmp variables to make code more readable:
    starting_date = data_of_simulation_period_void.index[0]
    
    T = data_of_simulation_period_void.index
    x = data_of_simulation_period_void["Close"].values
    x[0] = x0
    N = len(T)
    for i in range(N-1):
        dt = (T[i+1]-T[i]).days
        dWt = np.sqrt(dt) * rd.randn() 
        x[i+1] = x[i] + a(T[i],x[i])*dt + b(T[i],x[i])*dWt
    
    data_of_simulation_period_full = pd.DataFrame({"Close": pd.Series(x, index = T)})
    return data_of_simulation_period_full

def GBM(mu, sigma, x0,data_of_simulation_period_void):    

    T = data_of_simulation_period_void.index
    x = data_of_simulation_period_void["Close"].values
    x[0] = x0
    N = len(T)
    for i in range(N-1):
        drift = (mu - 0.5 * sigma**2) * (T[i]-T[0]).days
        Wt =   rd.randn()
        diffusion = sigma * Wt 
        x[i+1] = x[0]*np.exp(drift + diffusion)
    
    data_of_simulation_period_full = pd.DataFrame({"Close": pd.Series(x, index = T)})
    return data_of_simulation_period_full

