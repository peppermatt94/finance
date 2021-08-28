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
    @given(data_frames(index=indexes(elements=st.datetimes(min_value=pd.Timestamp(2019, 1, 1),
            max_value=pd.Timestamp(2020, 9, 1)),  min_size=15, unique=True),
            columns=[column("Close", elements = st.floats( allow_nan = True, allow_infinity=False), dtype=float),
            column("longName", elements = st.text(alphabet = 'p',min_size = 2, max_size = 2))]))
    @settings(deadline=None)
    def test_drop_nan(self,x):
        x = x.sort_index()
        x[x.Close<0.1] = 0.1   # i put some upper and lower limit on the data created
        x[x.Close>1000] = 1000
        x.longName = "prova"
        x.to_csv("simulation.csv")
        code_output = subprocess.run("finance --input simulation.csv ito --BM 100", capture_output = False)
        self.assertEqual( code_output.returncode, 0)
    
    #@unittest.skip("demonstrated")    
    def test_tick_list_folder_independence(self):
        folder1 = subprocess.run("finance --list_of_companies", capture_output = False)
        os.chdir("C:\\")
        folder2 = subprocess.run("finance --list_of_companies",capture_output = False)
        self.assertEqual([folder1.returncode,folder2.returncode], [0,0])
        
    def test_output_file_correctly_created(self):
        file = 'file.csv'
        subprocess.run(f"finance --output {file}", capture_output = False)
        if os.path.exists(file):
            database = pd.read_csv(file)   
            columns = database.columns
            columns = columns.to_list()
        self.assertEqual(columns, ['Date','Open','High','Low','Close','Volume','Dividends','Stock Splits','longName'])
        
    def test_output_file_ito_simulation_correctly_created(self):
        file = 'file.csv'
        subprocess.run(f"finance --company msft --output {file} ito --BM 100", capture_output = False)
        if os.path.exists(file):
            database = pd.read_csv(file)   
            columns = database.columns
            columns = columns.to_list()     
        self.assertEqual(columns, ['Unnamed: 0','Close','longName'])
        
    def test_logging_file_created_in_script_dir(self):
        subprocess.run("finance", capture_output = False)
        self.assertTrue(os.path.exists("../finance/finance.log"))
