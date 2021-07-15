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
from simulation import GBM, BM, Levy
from datetime import datetime

def main():
    import argparse
    from colorama import init
    init()  #init() enable windows powershell to ANSI string format
    
    ciao = sys.argv[1:]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='possible actions', dest='subparser')
   
    parser.add_argument("--company", 
        help="Select a company with its name or its " +
             "ticker. --list-of-companies for a list " + 
             "of companies and tickers",
        default = "msft")
    parser.add_argument("--list-of-companies", 
        help="Select a company with its name or its " +
             "ticker. --list-of-companies for a list " + 
             "of companies and tickers", action='store_true')
    
    ito = subparsers.add_parser("ito", 
        help= "Simulate the next 3 of 6 months of "+
              "the stock of the company with ITO process")
    
    ito.add_argument("--BM", type = int, 
        help="Select the brownian motion as ITO process: \n"+
             "dX_t = drift*dt + vol*dW_t \ndrift and vol "+
             "are computed from company data")
    
    ito.add_argument("--GBM", type = int,
       help="Select the brownian motion as ITO process: \n"+
             "dX_t = drift*X_t*dt + vol*X_t*dW_t \ndrift "+
             " and vol are computed from company data")#, default = "n")
    
    ito.add_argument("--levy", type = int,
       help="Select the brownian motion as ITO process: \n"+
             "dX_t = drift*dt + vol*dW_t + dJ_t \ndrift "+
             " and vol are computed from company data. Here" +
             "dJ_t is a poissonian random variable that create"+
             "a jump: you can pass jump and jump size as parameters")#, default = "n")
    
    graphix = subparsers.add_parser("graphix", 
        help="the subcommand that call graphical instrument of program")
    
    graphix.add_argument("--stocks",
        help= "show the variation of stock price of the company",action='store_true')
    
    graphix.add_argument("--dReturns",
        help= "show the variation of stock price of the company",action='store_true')
    
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
        
    #ito subcommands options:    
    
    #Brownian Motion
    if args.subparser == "ito":
        if args.BM != None:
            simulation = BM(args.BM, company_info)
            
        #Geometric Brownian Motion
        if args.GBM != None:
            simulation = GBM(args.GBM, company_info)
        
        #Levy process
        if args.levy != None:
            simulation = Levy(args.levy, company_info)
    
    if args.subparser == "graphix":
        # graphix subcommand options:
        if args.stocks:
            DA.plot_stocks_data(company_info, yf.Ticker(args.company).info["longName"])
            
        if args.dReturns:
            DA.plot_daily_returns_stats(company_info,  yf.Ticker(args.company).info["longName"])
            
        
if __name__=='__main__':
    main()