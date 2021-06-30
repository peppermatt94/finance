# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:22:21 2021

@author: pepermatt94


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
import numpy.random as rnd


def euler_maruyama(a,b,x0,T):    #Integration of the black scholes equation: ITO process
    '''Integration of the black scholes equation: ITO process
    
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
        A step furhter in the ITO process
        '''
    N = len(T)
    x = np.zeros((N,len(x0)))
    x[0] = x0
    for i in range(N-1):
        dt = T[i+1]-T[i]
        dWt = np.random.normal(0,dt)
        x[i+1] = x[i] + a(T[i],x[i])*dt + b(T[i],x[i])*dWt
    return x
 
Starting_File = "file with data analyzed with snakemake"

volatility = "something_get_from_data"
Expected_Rate_Of_Return =  "something_else_get_from_data"

T = 100
dt = "someting"                                        #"small period of time"
epsilon = rnd.randn(T)                #"Wiener variable"

#dSOverS = Expected_Rate_Of_Return*dt +volatility*epsilon*np.sqrt(dt)

