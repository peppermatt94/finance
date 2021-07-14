# -*- coding: utf-8 -*-
"""

Ideas for the following program:

    Montecarlo simulation for pricing,
    Command Line Interface program
    I 'll write something and i hope something work

"""
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import yfinance as yf #yahoo finance API to download economic database
import sys
import os
sys.path.append(os.getcwd())
import DataAnalyzers as DA
from simulation import Euler_Maruyama, GBM
from datetime import datetime

def main():
    import argparse
    from colorama import init
    init()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='possible actions', dest='subparser')
   
    parser.add_argument("--company", help="Select a company with its name or its" +
                        " ticker. -list-of-companies for a list of companies and tickers",
                        default = "msft")
    parser.add_argument("--showGraph", help="allows you to plot the data of the"+
                        "selected period of the stocks", default = "n")
    ito = subparsers.add_parser("ito", help= "Simulate the next 3 of 6 months of "+
                        "the stock of the company with ITO process")
    ito.add_argument("--simulate", help="allows you to plot the data of the"+
                        "selected period of the stocks")
    GBM = subparsers.add_parser("--GBM", help= "Simulate the next 6 months of "+
                        "the stock of the company with linear regression ML")#, action = "ito")
    GBM.add_argument("--showGraph", help="allows you to plot the data of the"+
                        "selected period of the stocks")#, default = "n")
    levy = subparsers.add_parser("--levy", help= "Simulate the next 6 months of "+
                        "the stock of the company with levy process")#, action = "ito")
    levy.add_argument("--showGraph", help="allows you to plot the data of the"+
                        "selected period of the stocks")#, default = "n")
    args = parser.parse_args()
    """
    if args.company is not in listOfcompany:
        raise error
    """
    try:    
        company_info = yf.Ticker(args.company).history(period = "max")
    except:
        #Exception needed since sometimes yahoo finance put some limit of download
        print("\033[0;31m", end = " JSON error: yahoo finance have some problem. retry later!!")
        sys.exit()  
    
    
    
    if args.showGraph == "y":
        Period = 12 #default to change
        new = company_info.reset_index()
        fig, ax = plt.subplots()
        ax.plot(new.Date, new.Close)
        ax.set_title(f"STOCK OF LAST {Period} MONTHS OF {args.company}")
        ax.set_xlabel("DATA")
        ax.set_ylabel("STOCK PRICE ($)")
        ax.tick_params(axis="x", labelsize=10, labelrotation=20)
        plt.show()

    #Brownian Motion
    
    if args.subparser == "BM":
        period = 3
        mu, sigma = DA.mu_and_sigma_estimation(company_info)
        a = lambda x,y: mu
        b = lambda x,y: sigma
        #a pandas dataframe also for the simulated data is comfortable:
        simulated_data = pd.DataFrame({"Close": pd.Series(np.arange(0,period*30,1), #for now, i fullfill with fictois data the price column
                                    index = pd.date_range(company_info.index[-1], periods=period*30))})  #the index are the day of the next three months
        x0 = company_info["Close"].iloc[-1]                          #the starting point is the last data in the company_info
        simulated_data = Euler_Maruyama(a,b,x0, simulated_data)
        plt.plot(simulated_data.index,simulated_data.Close )
        plt.tick_params(axis="x", labelsize=10, labelrotation=20)
        plt.show()

    #Geometric Brownian Motion
    
    if args.subparser == "BM":
        period = 3
        mu, sigma = DA.mu_and_sigma_estimation(company_info)
        a = lambda x,y: mu
        b = lambda x,y: sigma
        #a pandas dataframe also for the simulated data is comfortable:
        simulated_data = pd.DataFrame({"Close": pd.Series(np.arange(0,period*30,1), #for now, i fullfill with fictois data the price column
                                    index = pd.date_range(company_info.index[-1], periods=period*30))})  #the index are the day of the next three months
        x0 = company_info["Close"].iloc[-1]                          #the starting point is the last data in the company_info
        simulated_data = Euler_Maruyama(a,b,x0, simulated_data)
        plt.plot(simulated_data.index,simulated_data.Close )
        plt.tick_params(axis="x", labelsize=10, labelrotation=20)
        plt.show()


    #Levy process
    
    if args.subparser == "BM":
        period = 3
        mu, sigma = DA.mu_and_sigma_estimation(company_info)
        a = lambda x,y: mu
        b = lambda x,y: sigma
        #a pandas dataframe also for the simulated data is comfortable:
        simulated_data = pd.DataFrame({"Close": pd.Series(np.arange(0,period*30,1), #for now, i fullfill with fictois data the price column
                                    index = pd.date_range(company_info.index[-1], periods=period*30))})  #the index are the day of the next three months
        x0 = company_info["Close"].iloc[-1]                          #the starting point is the last data in the company_info
        simulated_data = Euler_Maruyama(a,b,x0, simulated_data)
        plt.plot(simulated_data.index,simulated_data.Close )
        plt.tick_params(axis="x", labelsize=10, labelrotation=20)
        plt.show()
if __name__=='__main__':
    main()