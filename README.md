# Finance
## A CLI to download, analyze and simulate economic data

**Finance** is a CLI designed for economics simulation and analysis.
It use the yahoo finance REST API to download economic data.
One can select a company from those presents in the yahoo finance database 
(see documentation) and from that one can make ITO simulations:
brownian motion simulation, geometric brownian motion and 
levy motion.



# Installing Finance

To install **Finance**:
```
git clone https://github.com/peppermatt94/finance
pip install finance
```
and it's done.

# dependencies

In order to use **Finance** the following packages should be enough:

* python>3.7
* matplotlib
* numpy
* scipy
* yfinance
* pandas

They are already embedded in the installation in the `setup.py`. If you want to be sure all dependencies are installed, you can
do:
```
cd finance
pip install requirements.txt
```
# Getting Started

TO get the first output from ***Finance***  type:
```
finance
```
The program will start to work with the default commands.
It will download Microsoft Corporation stocks from yahoo finance and 
will save it on a file called `finance.csv`.

In order to get help about the command of the program the usual commands
```
finance --help
```
is available.

## Input and Output data

As a default, **Finance** have the Microsoft corporation data from yahoo finance
API as input. Neverthless, the program have the ability to select another company
from online database or from local PC, assuming that the local file is well formatted to interface 
with the program. Let's analyze first the online database download command.

To say to the program to download a database, the command `--company` is given.
It take as argument the tick of the companies you are searching for in the yahoo finance
database. A correct question can be: how can i know what is the tick of the company i'm
searching for in the cloud? A good question. For this purpose, there are two step that solve
almost ever the problem. First step is to check if your company is from that listed by the 
command `--list_of_companies`. If your company is not there, you can appeal to a Google search, 
`company name yahoo tick` and the problem is fix. 

Another possible input is a local database. The name of the database can be passed
to the command `--input <path\to\file.ext>`. If the file is in the workng directory
you don't need to pass all the path, but only the name of the file (and the extension).
This command is very helpfull to use the program in a kind of pipe mode.

Output file can be controlled by the `--output <path/to/output.ext>` command. Notice that 
there is a default value of this command, in the file `finance.csv`. This means that the program
*ever* create a file output, but only one output is available. This means, for instance, that one
cannot distringuish between the output of the simulation or the output of the historycal data. If you
want to distinguish it, you must run the program twice with two different output files.
A correct question can be: and how can i know what is the data i'm putting in the file? The answer is: the last
data the program generate: if you do not perform an ITO simulation, on the file you will find historycal data. But if
you perform ITO simulation, on the file you will find simulated data. 

In order to store the name of company, on the file there will be another column called "name".
An example of usage
```
finance --company TSLA --output Tesla_Stocks.csv
```
will download Tesla data and save it in Tesla_Stocks.csv file. 

## ITO simulations

The ITO simulations have a central role in the program.  
On the base of the input Data the program can perform three different type of simulation:
* Brownian Motion
* Geometric Brownian Motion
* Levy process

In the project is implemented the simulation.py package to perform ITO simulation.
It can be used also as independent package, but for now, it was implemented for this
particular utility and it was not test for independent use.

In order to start the simulation, the subcommand 'ito' must be called.
As usual
```
finance ito --help
```
give you the help of the command.

To start the simulation, one can select one the three possible commands as follow:
```
finance ito --BM <number-of-days>
finance ito --GBM <number-of-days>
finance ito --levy <number-of-days>
```
The argument if the commands are the number of day i whic you want to perform simulation.
An example of usage can be:
```
finance --company amzn ito --BM 100
```
do a brownian motion simulation that start from the last data 
in the amazon historical data and simulate 100 days, almost three
months of stock price motion. 

Remember: even if you do not select an output, the program creates an output in finance.csv file.
I advice to select ever an output, and use the program in a pipe style with graphix subcommand

## Graphix

The `graphix` subcommand allow you to get a graphical output of stock or simulation. 
It take the input file (see input and output) and create stocks price graph with the
`--stocks` command or dayly returns histogram with the `dReturns` command.
The usual command: 
```
finance graphix --help
```
is available. 

An very simple example of usage is (exployting the default options of Microsoft stocks input) :
```
finance graphix --stocks
```
Have as output:
![alt text](https://github.com/peppermatt94/finance/blob/main/img/stocks.png)
while:
```
finance graphix --dReturns
```
Have as output:
![alt text](https://github.com/peppermatt94/finance/blob/main/img/dReturns.png)
This subcommand is tought in particular to be used at the end of a pipe:
```
finance --company amzn --output amazon_stock.csv ito --BM 100 ; finance --input amazon_stock.csv graphix --stocks
```
It is not a proper pipeline, but actually it is a process that can be authomatized.

# Contacts

## Author: 
Matteo Peperoni
matteo.peperoni@libero.it
Alma Mater Università di Bologna
