import pandas as pd
import numpy as np

data_path = {
    'TEST 3 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-1-3PARTS-07-12-2023.csv',
    'TEST 10 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-3-10PARTS-07-12-2023.csv',
    'TEST 12 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-4-12PARTS-07-12-2023.csv',
    'TEST 15 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-2-15PARTS-07-12-2023.csv'    
}

data = pd.read_csv(data_path['TEST 10 PARTS'], sep=";", header=0, decimal=',')
print(data)