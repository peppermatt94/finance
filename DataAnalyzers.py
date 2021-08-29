# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib as mpl
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from simulation import ITO_simulation
from scipy.stats import norm

def set_blue_and_red_triangle(xlims, ylims, up_or_down):
    """
    This function is needed to create the correct
    coordinate to insert daily returns triangles in
    plot if the return is positive or negative

    Parameters
    ----------
    xlims: bidimensional vector:
        The xlim of the graph you created

    ylims: bidimensional vector
        The ylim of the graph you created

    up_or_down: string:
        It is different if you want a triangle with upward or downward angle.
        This flag need to fix this direction.
        Possible values: 'up' or 'down'

    Returns
    -------
    Coordinates for the triangles, to place triangles in the top left
    of the graph
    """
    if up_or_down == "up":
        xLength = xlims[1]-xlims[0]
        yLength = ylims[1]-ylims[0]
        ax = xlims[0] +  xLength/10
        bx = ax + xLength/20
        cx = (ax+bx)/2
        ay = ylims[0] + 9*yLength/10
        by = ay
        cy = ay + yLength/15

    if up_or_down == "down":
        xLength = xlims[1]-xlims[0]
        yLength = ylims[1]-ylims[0]
        ax = xlims[0] +  xLength/10
        bx = ax + xLength/20
        cx = (ax+bx)/2
        ay = ylims[0] + 9*yLength/10
        by = ay
        cy = ay - yLength/15

    return np.array([[ax, ay], [bx, by], [cx, cy]])

def today_return(df):
    '''
    Compute the return of the last two day in the stock price in order
    to get if the company is gaining or loosing credits.

    Parameters
    ----------
    df : Pandas.Dataframe
        The downloaded or simulated Data

    Returns
    -------
    today_return : float
        The return in price in today stock

    PercentodayReturn : float
        The return in percentage in today stock.

    '''
    todayReturn = df["Close"].iloc[-1]-df["Close"].iloc[-2]
    PercentodayReturn = (todayReturn/df["Close"].iloc[-1])*100
    return  today_return, PercentodayReturn

def plot_stocks_data(df, name):
    """
    plot stocks Data.

    Parameters
    ----------
    df : pandas.DataFrame
        The downloaded or simulated Data.
    name: str.
        The name of the company in question
    Returns
    -------
    None.

    """

    df = df.reset_index() #  i need to reset index since i want to use Date (index)
                          #  as column
    #PLOTTING
    mpl.style.use('ggplot')
    fig, ax = plt.subplots()
    ax.plot(df.Date, df.Close)
    ax.set_title(f"STOCKS OF {name}")
    ax.set_xlabel("DATA")
    ax.set_ylabel("STOCK PRICE ($)")
    ax.tick_params(axis="x", labelsize=10, labelrotation=20)

    todayReturn, percentTodayReturn = today_return(df)
    PositiveReturn = percentTodayReturn > 0
    # I need it here also for the direction of triangle
    # if it is positive, direction upward, if negative,
    # direction downward

    patches = []  # the two triangles are patches
    #preparing parameters for the patches coordinates and transparency
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()

    X = set_blue_and_red_triangle(xlims, ylims, "up") # Patch coordinates

    if PositiveReturn:
        alpha = 1
    else:
        alpha = 0.05   # Patch transparency

    polygon = Polygon(X, True, color=[0.5, 0.5, 0.2], alpha=alpha) # Patch
    patches.append(polygon)

    X = set_blue_and_red_triangle(xlims, ylims, "down")# Patch coordinates

    if PositiveReturn:
        alpha = 0.05
    else:
        alpha = 1    # Patch transparency

    polygon = Polygon(X, True, color=[1, 0, 0], alpha=alpha)# Patch
    patches.append(polygon)

    p = PatchCollection(patches, match_original=True)
    ax.add_collection(p)

    ax.annotate('{0:+}'.format((round(percentTodayReturn, 2)))+"%", # i need to put the annotation
                xy=(X[0][0]+(xlims[1]-xlims[0])/15, X[0][1])) # near the triangles
    plt.show()


def plot_daily_returns_stats(df, name):
    """
    plot of stocks Data, with
    information about simulation,
    mu, sigma, and today return.

    Parameters
    ----------
    df : pandas.DataFrame
        The downloaded or simulated Data.

    name: str.
        The name of the company in question
    Returns
    -------
    None.

    """
    mpl.style.use('classic')# as column
    fig, ax = plt.subplots()

    # i use the methods daily_return from ITO_simulation class
    daily_returns = ITO_simulation(1, df).daily_return()

    #plot the historgram
    ax.hist(daily_returns, density=True, bins=50)

    #Fit of the distribution with scipy.stats pacakge
    mu, std = norm.fit(daily_returns)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)

    #plot of the distribution too
    ax.plot(x, p, 'k', linewidth=2)
    ax.set_title(f"DAILY RETURNS DISTRIBUTION OF {name}")
    ax.set_xlabel("RETURNS")
    ax.set_ylabel("COUNT")

    #info in the graph
    mu = "{:.2e}".format(mu)
    std = "{:.2e}".format(std)
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    ax.text(xlims[0] + (xlims[1]-xlims[0])/10, ylims[0] +7*(ylims[1]-ylims[0])/10,
            r"$\mu =$"+mu +"\n" + r"$\sigma =$" +std, style='italic', fontsize=16,
            bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10})
    plt.show()