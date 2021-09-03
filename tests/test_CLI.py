import pandas as pd
import numpy.random as rn
from hypothesis import given, settings
import hypothesis.strategies as st
from hypothesis import assume
from hypothesis.extra.pandas import column, data_frames,range_indexes, series, indexes,columns
import subprocess
import unittest
import os 

class CLI_Tests(unittest.TestCase):
    #@unittest.skip("demonstrated")
    def test_BMcommand_work(self):
        '''
    Given :
        - command to perform BM simulation output for 100 days.
    And :
        - assert the program execute without problem (exit 0)'
    '''    
        BM_output = subprocess.run("finance --company msft --output 'simulation.csv' ito --BM 100 ", stdout=subprocess.DEVNULL)
        self.assertEqual(BM_output.returncode, 0)
        
    def test_GBMcommand_work(self):
        '''
    Given :
        - command to perform GBM simulation output for 100 days.
    And :
        - assert the program execute without problem (exit 0)'
    '''    
        GBM_output = subprocess.run("finance --company msft --output 'simulation.csv' ito --GBM 100 ", stdout=subprocess.DEVNULL)
        self.assertEqual( GBM_output.returncode,0)
        
    def test_levycommand_work(self):
        '''
    Given :
        - command to perform levy simulation output for 100 days.
    And :
        - assert the program execute without problem (exit 0)'
    '''    
        levy_output = subprocess.run("finance --company msft --output 'simulation.csv' ito --levy 100", stdout=subprocess.DEVNULL)
        self.assertEqual( levy_output.returncode, 0)
    
    def test_graphix_stockcommand_work(self):
        '''
    Given :
        - command to perform stock graph.
    And :
        - assert the program execute without problem (exit 0)'
    '''    
        graphix_stock_output = subprocess.run("finance --input 'simulation.csv' graphix --stocks", stdout=subprocess.DEVNULL, capture_output=False)
        self.assertEqual( graphix_stock_output.returncode, 0)
   
    def test_graphix_dReturnscommands_work(self):
        '''
    Given :
        - command to perform the daily return graph.
    And :
        - assert the program execute without problem (exit 0)'
    '''    
        graphix_dreturn_output = subprocess.run("finance --input 'simulation.csv' graphix --dReturns", stdout=subprocess.DEVNULL,capture_output=False)
        self.assertEqual(  graphix_dreturn_output.returncode, 0)
         
    #@unittest.skip("demonstrated")    
    def test_tick_list_folder_independence(self):
        '''
    Given :
        - program ran list_of_company command in different folders.
    And :
        - assert the  program execute without problem (exit 0)'
    '''    
        folder1 = subprocess.run("finance --list_of_companies", stdout=subprocess.DEVNULL)
        os.chdir("C:\\")
        folder2 = subprocess.run("finance --list_of_companies",stdout=subprocess.DEVNULL)
        self.assertEqual([folder1.returncode,folder2.returncode], [0,0])
        
    def test_output_file_correctly_created(self):
        '''
    Given :
        - program create an output file in file.csv.
    And :
        - assert the  program create the file in current folder'
    '''    
        file = 'file.csv'
        subprocess.run(f"finance --output {file}", stdout=subprocess.DEVNULL)
        self.assertTrue(os.path.exists(file))
        database = pd.read_csv(file)   
        columns = database.columns
        columns = columns.to_list()
        self.assertEqual(columns, ['Date','Open','High','Low','Close','Volume','Dividends','Stock Splits','longName'])
        
     
    def test_output_file_ito_simulation_correctly_created(self):
        '''
    Given :
        - program create an output file of the ito simulation .
    And :
        - assert the program create the file correcly in the current folder
        - assert the program create the file with well formatted columns'
    '''    
        file = 'file.csv'
        subprocess.run(f"finance --company msft --output {file} ito --BM 100", stdout=subprocess.DEVNULL)
        self.assertTrue(os.path.exists(file))
        database = pd.read_csv(file)   
        columns = database.columns
        columns = columns.to_list()     
        self.assertEqual(columns, ['Unnamed: 0','Close','longName'])
        
    def test_logging_file_created_in_script_dir(self):
        subprocess.run("finance", stdout=subprocess.DEVNULL )
        self.assertTrue(os.path.exists("../finance/finance.log"))