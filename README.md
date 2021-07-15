# Finance
## A CLI to download, analyze and simulate economic data

**Finance** is a CLI designed for accademic purpose.
 It use the yahoo finance REST API to download economic data.
One can select a company from those presents in the yahoo finance database 
(see documentation) and from that one can make ITO simulations:
brownian motion simulation, geometric brownian motion and 
levy motion.

# Current Build Status
main branch **pass**

# Installing Finance

To install **Finance**:
```
git clone https://github.com/peppermatt94/finance
pip install finance
```
and it's done.

# dependencies

In order to use **Finance** one need some packages already 
install:

-python>3.7
-matplotlib
-scipy
-yfinance
-pandas

to install all dependencies:
```
cd finance
pip install requirements.txt
```
# Getting Started

Finance CLI is thought as a dependent utility. Without a minimal
pipeline, the output the user see are very few. 
If you write:
```
finance
```
you don't get anything on screen, even if the program execute all
commands without problem.

In order to get help about the command of the program write
```
finance --help
```

From this command, one can see that the positional arguments '--company'
accept as argument the tick of a company as presents in the yahoo finance
database. In order to get a list of tick the command '--list-of-company'.
The default company is Microsoft Corporation, with the tick 'msft'. If 
you want to download Tesla Motors stocks, just put:
```
finance --company TSLA
```
and the data are downloaded and offered in the stdout. 
To save it 
```
finance --company TSLA > TSLA.txt
```

## ITO simulation

The principle part of the programs are the ITO simulation made 
on the base of the data downloaded from yahoo finance. The simualtion
use the 'simulation.py' package, in which is implemented the
class ITO_simulation. 
In order to start the simulation, the subcommand 'ito' must be called.
```
finance ito --help
```
from the help function one can see there are threee different possible 
simulation:
```
finance ito --BM <number-of-days>
finance ito --GBM <number-of-days>
finance ito --levy <number-of-days>
```
that are the three flag for the three possible simulations: levy, 
browninan motion, geometric brownian motion. They take as argument
the number of days of the simulation. For instance:
```
finance --company amzn ito --BM 100
```
do a brownian motion simulation that start from the last data 
in the amazon historical data and simulate 100 days, almost three
months of stock price motion. 

The simulation give as output a datafrae to be used for pipelin or
for plotting

## Graphical output

In order to get some graphical output, the 'graphix' subcommand
was implmented. It take the output of simulation or download and
create stocks price graph or dayly returns histogram. This last
graph is usefull in particulare to understand if the selected
samples have statistical limit. 
```
finance graphix --stocks
```
Have as output:
```
finance graphix --dReturns
```
Have as output:
This subcommand is tought to be used at the end of a pipeline.
```
finance --company amzn ito --BM 100 | finance graphix --stocks
```
# Contacts

## Author: 
Matteo Peperoni
matteo.peperoni@libero.it
Alma Mater Università di Bologna
