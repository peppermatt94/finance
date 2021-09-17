from numpy import random as rd
from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class ITO_simulation:
    """
    Principle class: it take the pandas dataframe of the stock prices
    and the number of days in which the simulation must be perfomed.
    ITO processes are extended class of this one.

    Parameters
    -----------
    number_of_days : the period of the simulation expressed in number
                    of days
  
    data_of_period: the historical data of the company.
    
    Methods
    ------------
    T : create a data range from the final date in data_of_period and the
        period present in number_of_days
    
    daily_return : return a list that contain the difference, in each day, between the today price
            and the yesterday price
            
    mu_and_sigma_estimation: method that estimate mu and sigma from historycal data
    
    Euler_Maruyama : the proper simulation method, it embeds all the methods
                     in order to do ito simulation with euler_maruyama approximation 
    """
    number_of_days: int
    data_of_period: pd.DataFrame()

    __version__ = (0, 1, 0)

    def T(self):
        """
        Parameters
        ----------
        self : ITO_simulation instance. In particular you need the
             number of days to get the datetime index
        Returns
        -------
        A date range from the final date in data_of_period and the
        period present in number of step.

        """
        starting_date = self.data_of_period.index[-1]
        return pd.date_range(starting_date, periods=self.number_of_days)

    def daily_return(self):
        '''Estimation of the expected return from known data

        Parameters
        ----------
        self : ITO_simulation instance. In particular, you need here
            "Close" column of "data_of_period", in which are
            conserved the historical stock price data.

        Returns
        -------
        A list of returns, i.e. the difference, in each day, between the today price
            and the yesterday price.

        References
        ----------
        J.C.Hull, Options, futures and others derivatives, ch. 7.

        '''
        self.data_of_period = self.data_of_period.dropna() # i need some brute force for nan error.
        Close_prices = self.data_of_period["Close"].values
        returns = []
        for i in range(0, len(Close_prices)-1):
            today = float(Close_prices[i+1])   # i need some brute force for casting errors
            yesterday = float(Close_prices[i])
            if yesterday != 0:
                daily_return = (today - yesterday)/yesterday
                returns.append(daily_return)
        return returns

    def mu_and_sigma_estimation(self):
        '''Estimation of the volatility from the known data
        Parameters
        ----------
        self : ITO_simulation instance.

        Returns
        -------
        Expected returns mu (also named 'drift' in brownian process)
        and Volatility predicted by the data_of_period in the
        ITO_simulation instance

        References
        ----------
        J.C.Hull, Options, futures and others derivatives, ch. 7.
        '''
        returns = self.daily_return()
        mu = np.mean(returns)           # drift coefficient
        sigma = np.std(returns)         #volatility coefficient
        return mu, sigma


    def Euler_Maruyama(self):
        '''Integration of the ITO process. Here i use euler-maruyama approximation

        Parameters
        ----------
        self : ITO_simulation instance. Actually, it need in particular
            self.T as the period in which the simulation is performed
            and self.data_of_period to get mu and sigma

        Returns
        -------
        data_of_simulation_period filled with a certain ITO process,
        by the euler-maruyama approximation

        References
        https://en.wikipedia.org/wiki/Euler%E2%80%93Maruyama_method
        '''
        #I use two tmp variables to make code more readable:
        x0 = self.data_of_period["Close"].iloc[-1]
        T = self.T()
        x = np.empty(self.number_of_days)
        x[0] = x0
        for i in range(self.number_of_days-1):
            dt = (T[i+1]-T[i]).days
            t = (T[i+1]-T[0]).days
            dWt = np.sqrt(dt) * rd.randn()

            if hasattr(self, "jump"):
                intensity = self.jump_intensity_func(t, x[i])
                N = rd.poisson(intensity*dt)
                jump_addend = N*self.jump_size
            else:
                jump_addend = 0
            x[i+1] = x[i] + self.drift(t, x[i])*dt + self.vol(t, x[i])*dWt +jump_addend

        data_of_simulation_period_full = pd.DataFrame({"Close": pd.Series(x, index=T)})

        return data_of_simulation_period_full
@dataclass
class BM(ITO_simulation):
    """Simulate a drifted Brownian motion
    dX_t = drift*dt + vol*dW_t
    where drift and vol are real numbers
    """
    number_of_days: int
    data_of_period: pd.DataFrame()
    _drift: float = 0 #Default value changed in __post_init__
    _vol: float = 0

    def __post_init__(self):
        self._drift = self.mu_and_sigma_estimation()[0]
        self._vol= self.mu_and_sigma_estimation()[1]

    def drift(self, t, x) -> float:
        return self._drift

    def vol(self, t, x) -> float:
        return self._vol

@dataclass
class GBM(ITO_simulation):
    """Simulate a drifted Geometric Brownian motion
    dX_t = drift*X_t*dt + vol*X_t*dW_t
    where drift and vol are real numbers
    """
    number_of_days: int
    data_of_period: pd.DataFrame()
    _drift: float = 0
    _vol: float = 0

    def __post_init__(self):
        self._drift = self.mu_and_sigma_estimation()[0]
        self._vol= self.mu_and_sigma_estimation()[1]


    def drift(self, t, x) -> float:
        return self._drift * x

    def vol(self, t, x) -> float:
        return self._vol * x

@dataclass
class Levy(ITO_simulation):
    """Ito_diffusion to simulate a Levy process
    dX_t = drift*dt + vol*dW_t + dJ_t
    where drift and vol are real numbers, dJ_t a poissonian variable
    that create a jump.
    """
    number_of_days: int
    data_of_period: pd.DataFrame()
    _drift: float = 1
    _vol: float = 0
    jump: float = 0.01      # the default values are there to give an idea
    jump_size: float = 0.1  # of the order of magnitude of the values

    def __post_init__(self):
        self._drift = self.mu_and_sigma_estimation()[0]
        self._vol= self.mu_and_sigma_estimation()[1]

    # Here i assume the jump intensity doesn't depend on time
    # and space. Future development could evaluate a property.setter
    # in which one can pass a callable
    def jump_intensity_func(self, t, x) -> float:
        return self.jump

    def drift(self, t, x) -> float:
        return self._drift

    def vol(self, t, x) -> float:
        return self._vol
