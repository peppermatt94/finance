# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import pandas as pd
import scipy.stats as st
import yfinance #yahoo finance API to download economic database


def volatility_estimation(data_in_period):
    '''Estimation of the volatility from the known data
    
    Parameters
    ----------
    data_in_period : Pandas dataframe
        Here must be conserved the stock price data connected to time period.
        This means that the index of the dataframe must be datetime, and a 
        column must be named "Close", the close price of the option
    Returns
    -------
    Volatility predicted by the data_of_period
    
    References
    ----------
    J.C.Hull, Options, futures and others derivatives, ch. 7.
    '''
    if len(data_in_period.index) < 10:
        raise "I cannot compute volatility with so few data"
        return None
    #Extrapolate the period in question by the data index
    period = data_in_period.index[-1]-data_in_period.index[0]
    period = period.days
    dt = (data_in_period.index[1]-data_in_period.index[0]).days
    #In date_of_a_period["Close"] must be recorded the closed price of stock
    #in a certain period. u is the difference between the logaritmic price 
    #in two consecutive step
    uList = np.zeros(len(data_in_period["Close"]))
    for count in range(len(data_in_period["Close"])):
        uList[count] = np.log(data_in_period["Close"].iloc[count]/data_in_period["Close"].iloc[count-1])
    
    #The volatility is associated to the standard deviation of u, divided for the period
    s = np.var(uList)
    mu = np.mean(uList)
    
    sigma = s/np.sqrt(abs(dt))
    return sigma, mu
    
def expected_return_estimation(data_in_period, volatility):
    '''Estimation of the expected return from known data
    

    Parameters
    ----------
    data_in_period : pandas_dataframe
        Here must be conserved the stock price data connected to time period.


    Returns
    -------
    Expected return predicted from data_in_period.
    References
    ----------
    J.C.Hull, Options, futures and others derivatives, ch. 7.

    '''
    #Since we assume an exponential behaviour for the price at time T respect
    #to price at time t=0 ( E(S_T) = S_0exp(muT)), with mu expected return
    #usually mu is estimated consider only S_0 and S_T and subracting mu with volatility
    
    period = data_in_period.index[-1]-data_in_period.index[0]
    mu = np.log(data_in_period["Close"].iloc[-1]/(data_in_period["Close"].iloc[0]))
    
    return mu + volatility**2/2

def daily_return(Close_prices):
    '''Estimation of the expected return from known data

    Parameters
    ----------
    Close_prices : Series
        Here must be conserved the historical stock price data.

    Returns
    -------
    A list of returns, i.e. the difference, in each day, between the today price
    and the yesterday price.
    References
    ----------
    J.C.Hull, Options, futures and others derivatives, ch. 7.

    '''
    returns = []
    for i in range(0, len(Close_prices)-1):
        today = Close_prices[i+1]
        yesterday = Close_prices[i]
        daily_return = (today - yesterday)/yesterday
        returns.append(daily_return)
    return returns


def mu_and_sigma_estimation(data_in_period):
    '''Estimation of the volatility from the known data
    
    Parameters
    ----------
    data_in_period : Pandas dataframe
        Here must be conserved the stock price data connected to time period.
        This means that the index of the dataframe must be datetime, and a 
        column must be named "Close", the close price of the option
    Returns
    -------
    Expected returns mu (also named 'drift' in brownian process)
    and Volatility predicted by the data_of_period
    
    References
    ----------
    J.C.Hull, Options, futures and others derivatives, ch. 7.
    '''
    returns = daily_return(data_in_period["Close"].values)
    mu = np.mean(returns)           # drift coefficient
    sigma = np.std(returns)*252 
    return mu, sigma

def plot_real_data():
    pass

def plot_simulated_data():
    pass