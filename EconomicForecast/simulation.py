
import numpy as np
import pandas as pd
import matplotlib.pylab as plt



def ITO_process(a,b,x0,T):    #Integration of the black scholes equation: ITO process
    '''Integration of the ITO process
    
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


