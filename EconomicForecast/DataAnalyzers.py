# -*- coding: utf-8 -*-
import sympy as sm
import numpy as np
import scipy as sp
import pandas as pd
import seaborn as sns
import pylab as plt
import scipy.stats as st
import yfinance #yahoo finance API to download economic database


def volatility_estimation(data_in_period):
    '''Estimation of the volatility from the known data
    
    Parameters
    ----------
    data_in_period : Pandas dataframe
        Here must be conserved the stock price data connected to time period.

    Returns
    -------
    Volatility predicted by the data_of_period

    '''
    #Extrapolate the period in question by the data index
    period = data_in_period.index[-1]-data_in_period.index[0]
    #In date_of_a_period["Close"] must be recorded the closed price of stock
    #in a certain period. u is the difference between the logaritmic price 
    #in two consecutive step
    u= [np.log(data_in_period["Close"].iloc[count]/data_in_period["Close"].iloc[count-1]) for count in len(data_in_period["Close"]) ]
    #The volatility is associated to the standard deviation of u, divided for the period
    s = np.std(u)
    sigma = s/np.sqrt(period)
    return sigma
    
def expected_return_estimation(data_in_period, volatility):
    '''Estimation of the expected return from known data
    

    Parameters
    ----------
    data_in_period : pandas_dataframe
        Here must be conserved the stock price data connected to time period.


    Returns
    -------
    Expected return predicted from data_in_period.

    '''
    #Since we assume an exponential behaviour for the price at time T respect
    #to price at time t=0 ( E(S_T) = S_0exp(muT)), with mu expected return
    #usually mu is estimated consider only S_0 and S_T and subracting mu with volatility
    
    period = data_in_period.index[-1]-data_in_period.index[0]
    mu = np.log(data_in_period["Close"].iloc[-1]/(data_in_period["Close"].iloc[0]))
    
    return mu - volatility/2

