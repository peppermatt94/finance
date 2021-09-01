# -*- coding: utf-8 -*-
from simulation import GBM, BM, Levy
from datetime import datetime
import DataAnalyzers as DA
import logging
import sys
import os
import numpy as np
import pandas as pd
import yfinance as yf #yahoo finance API to download economic database


dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.INFO, filename= dir_path + '\\finance.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

def progress(Text, color):
    #####################################
    color_output = {"green": "\u001b[32;1m", "red": "\u001b[31m", "Blue": "\u001b[34m", "No": ""}
    sys.stdout.write("\r."+" "*100) #Is needed to wash all the line
    text = u"\r" +color_output[color] +Text
    sys.stdout.write(text)
    sys.stdout.flush()
    logging.info(Text)
    ######################################

def error(Text):
    #####################################
    sys.stdout.write("\r."+" "*100) #Is needed to wash all the line
    text = u"\r\033[0;31m" +Text
    sys.stderr.write(text)
    sys.stdout.flush()
    logging.error(Text)
    exit(1)
    ######################################

def main():
    import argparse
    from colorama import init
    init()  #init() enable windows powershell to ANSI string format

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='subcommands of the program', dest='subparser')

    parser.add_argument("--company", "-co", help="Select a company for the download with its " +
                        "tick as argument",
                        default="msft")

    parser.add_argument("--list_of_companies", "-lco",
                        help="Show a short list of ticks associated to " +
                        "the extended name of the company", 
                        action='store_true')

    parser.add_argument("--input", "-i", type=str,
                        help="Take as argument the name of the file from which"+
                        "read the economic data", 
                        default=None)

    parser.add_argument("--output", "-o", type=str,
                        help="Take as argument the name of the file to which write"+
                        "the output of the program",
                        default="finance.csv")

    ito = subparsers.add_parser("ito",
                                help="ITO simulation for the choosen company. You "+
                                "must choose among brownian motion"+
                                "simulation, geometric brownian motion or levy")

    ito.add_argument("--BM", type=int,
                     help="Select the brownian motion as ITO process: \n"+
                     "dX_t = drift*dt + vol*dW_t \ndrift and vol "+
                     "are computed from company data")

    ito.add_argument("--GBM", type=int,
                     help="Select the brownian motion as ITO process: \n"+
                     "dX_t = drift*X_t*dt + vol*X_t*dW_t \ndrift "+
                     " and vol are computed from company data")

    ito.add_argument("--levy", type=int,
                     help="Select the brownian motion as ITO process: \n"+
                     "dX_t = drift*dt + vol*dW_t + dJ_t \ndrift "+
                     " and vol are computed from company data.")

    graphix = subparsers.add_parser("graphix",
                                    help="the subcommand that call "+
                                    "graphical instruments of the program")

    graphix.add_argument("--stocks", "-ss",
                         help="Plot the variation of stock price of the company",
                         action='store_true')

    graphix.add_argument("--dReturns", "-dr",
                         help="Plot the histogram of the daily return of the company",
                         action='store_true')

    args = parser.parse_args()

    if args.list_of_companies:
        try:
            listOfCompanies = pd.read_csv(dir_path + "\\tick.txt", sep=";")
            print(listOfCompanies.to_markdown())
        except:
            error("Problem in reading the ticks list!! Ensure that in the " + 
                  "script directory there is the file 'tick.txt'")
        sys.exit()  
        
    if args.input == None:
        try:  
            progress("Loading financial data from yahoo finance", "No")
            company_info = yf.Ticker(args.company).history(period="max").dropna()
            name_company = yf.Ticker(args.company).info["longName"]

        except:
            #Exception needed since sometimes yahoo finance put some limit of download
            error("Problem in downloading yahoo finance database.")
            progress("\nControl the syntax of the tick you passed and internet connection", "red")
            sys.exit()  
        
        progress("Store file in {}".format(args.output), "No")
        Data_to_save = company_info
        Data_to_save["longName"] = name_company
        Data_to_save.to_csv(args.output)
    else:
        try:
            progress("Loading financial data from {}".format(args.input), "No")
            company_info = pd.read_csv(args.input).dropna()
        except:
            error("Problem in reading input database")
            progress("\nControl if the file you passed actually exist", "red")
            sys.exit()

        Renaming_column = company_info.columns[0]
        company_info.rename(columns={Renaming_column: "Date"}, inplace=True)
        company_info["Date"] = pd.DatetimeIndex(company_info["Date"])
        company_info = company_info.set_index(["Date"])
        name_company = company_info["longName"].iloc[0]
    
    #ito subcommands options:    

    if args.subparser == "ito":
        if args.BM != None:
        #Brownian Motion
            progress("Starting ITO simulation BM", "No")
            simulation = BM(args.BM, company_info).Euler_Maruyama()
            simulation["longName"] = name_company + " BM simulation"
            simulation.to_csv(args.output)

        #Geometric Brownian Motion
        if args.GBM != None:
            progress("Starting ITO simulation GBM", "No")
            simulation = GBM(args.GBM, company_info).Euler_Maruyama()
            simulation["longName"] = name_company + " GBM simulation"
            simulation.to_csv(args.output)

        #Levy process
        if args.levy != None:
            progress("Starting ITO simulation levy", "No")
            simulation = Levy(args.levy, company_info).Euler_Maruyama()
            simulation["longName"] = name_company + " LEVY simulation"
            simulation.to_csv(args.output)

    if args.subparser == "graphix":
        # graphix subcommand options:
        if args.stocks:
            progress("Preparing the plot", "No")
            DA.plot_stocks_data(company_info, name_company)

        if args.dReturns:
            progress("Preparing the plot", "No")
            DA.plot_daily_returns_stats(company_info, name_company)

    progress("done", "green")
if __name__ == '__main__':
    main()