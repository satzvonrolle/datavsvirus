import unittest
import pandas as pd
import os


BASEDIR = '../../data/raw/italy/'
        
"""
🍝 Code (duplicate in convert_italy.py)
"""
def convert_to_datestring(name):
    date = name[6:10]
    month = int(date[:2])
    day = int(date[2:])
    return '%i/%i/20' % (month, day)

def extract_cases(name):
    df = pd.read_csv(BASEDIR + name)
    return df['totale_casi'].to_numpy()
"""
🍝 Code 
"""


class Test(unittest.TestCase):

    def test_rki_germany_samples(self):
    
        #
        # Check with some samples if number of cases is correct for germany and italy.
        #
        
        data_germany = pd.read_csv("../../data/raw/germany/germany.csv")
        self.assertGreater(data_germany["AnzahlFall"].sum() ,  16000)
        

        names = [name for name in os.listdir(BASEDIR) if name.endswith('.csv')]
        df_italy = pd.DataFrame( {convert_to_datestring(name): extract_cases(name) for name in names})
        self.assertEqual(df_italy["2/25/20"].sum() ,  322)
        
        #
        # Load current and deprecated data for germany. Check if numbers match.
        #
        
        data_germany = pd.read_csv("../../data/converted/germany.csv")
        data_germany_depreacted = pd.read_csv("../../data/converted/germany_deprecated.csv")
        self.assertEqual(data_germany["03/18/20"].sum(), data_germany_depreacted["3/18/20"].sum())

if __name__ == '__main__':
    unittest.main()
