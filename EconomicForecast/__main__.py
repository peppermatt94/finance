# -*- coding: utf-8 -*-
"""

Ideas for the following program:
    
    Montecarlo simulation for pricing,
    Command Line Interface program
    I 'll write something and i hope something work

"""
#import sympy as sm
#import numpy as np
#import scipy as sp
import pandas as pd
#import seaborn as sns
import matplotlib.pylab as plt
import scipy.stats as st
import yfinance as yf #yahoo finance API to download economic database
#import DataAnalyzers
#import simulation


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", help="Select a company with its name or its" +
                        " ticker. -list-of-companies for a list of companies and tickers",
                        default = "msft")
    parser.add_argument("--showGraph", help="allows you to plot the data of the"+
                        "selected period of the stocks", default = "n")
    parser.add_argument("--simulate", help= "Simulate the next 6 months of "+
                        "the stock of the company")
    
    args = parser.parse_args()
    """
    if args.company is not in listOfcompany:
        raise error
    """
    company_info = yf.Ticker(args.company)
    print(company_info.history().head())
    if args.showGraph == "y" or "yes":
        Period = 6 #default to change
        new = company_info.history( period = "3mo").reset_index()
        fig, ax = plt.subplots()
        ax.plot(new.Date, new.Close)
        ax.set_title(f"STOCK OF LAST {Period} MONTHS OF {args.company}")
        ax.set_xlabel("DATA")
        ax.set_ylabel("STOCK PRICE ($)")
        ax.tick_params(axis="x", labelsize=10, labelrotation=30)
        plt.show()
    #arg.simulate()
#ITO lemma 

if __name__=='__main__':
    main()