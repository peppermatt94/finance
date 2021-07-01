# -*- coding: utf-8 -*-
"""

Ideas for the following program:
    
    Montecarlo simulation for pricing,
    Command Line Interface program
    I 'll write something and i hope something work

"""
import sympy as sm
import numpy as np
import scipy as sp
import pandas as pd
import seaborn as sns
import pylab as plt
import scipy.stats as st
import yfinance #yhaoo finance api to download economic database


#IMPORT DATA AND FETCH






#ANALYZE 


def euler_maruyama(a,b,x0,T):    #Integration of the black scholes equation: ITO process
    '''Integration of the black-scholes equation: ITO process
    
        Parameters
        ----------
        a : callable
            The interest rate respect time a(x_t,t), x_t is vector position
        b : callable
            the volatility  respect time b(x,t), x_t is vector
        x0: float 
            starting value
        T: float
            time period
            
        Returns
        -------
        ITO simulation from start time to T
        '''
    N = len(T)
    x = np.zeros((N,len(T)))
    x[0] = x0
    for i in range(N-1):
        dt = T[i+1]-T[i]
        dWt = np.random.normal(0,dt)
        x[i+1] = x[i] + a(T[i],x[i])*dt + b(T[i],x[i])*dWt
    return x

Starting_File = "file with data analyzed with snakemake"

volatility = "something_get_from_data"
Expected_Rate_Of_Return =  "something_else_get_from_data"

T = np.arange(0,100,1)
dt = "someting"                                        #"small period of time"

a = lambda x,t : 0.2
b = lambda x,t: 0.9
x0=100

x = euler_maruyama(a,b,x0,T)
plt.plot(T,x)

#ITO lemma 
import requests

a = requests.get("https://pkgstore.datahub.io/core/natural-gas/daily_json/data/2e630ca50c39a1a3cf6c3aff57a1b132/daily_json.json")
print(a.content)
