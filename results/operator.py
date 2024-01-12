import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from sqlalchemy import create_engine
class Operator():
    def __init__(self):
        #----------------------------- Tassio's path -----------------------------------------------------
        # self.data_path = {  
        #     'TEST 3 PARTS'  : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-1-3PARTS-07-12-2023.csv',
        #     'TEST 10 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-3-10PARTS-07-12-2023.csv',
        #     'TEST 12 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-4-12PARTS-07-12-2023.csv',
        #     'TEST 15 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-2-15PARTS-07-12-2023.csv'    
        # }
        #------------------------------ Alexandre's path ------------------------------------------------
        self.data_path = {  
            'TEST 3 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-1-3PARTS-07-12-2023.csv',
            'TEST 10 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-3-10PARTS-07-12-2023.csv',
            'TEST 12 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-4-12PARTS-07-12-2023.csv',
            'TEST 15 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-2-15PARTS-07-12-2023.csv'     
        }
        # Offset seen on raw data
        self.data_offset = - 0.3
        # Threshold for zeroing values
        self.threshold = 0.6
        # How many zeros in a row is considered a pause
        self.threshold_zeros = 33
        # Flag for counting
        self.cycle_counter_flag = False

    def get_data(self, file_name):
        # Read CSV
        self.data = pd.read_csv(self.data_path[file_name], sep=";", header=0, decimal=',')
         # Invert Index
        self.data = self.data[::-1].reset_index(drop=True)
        # Consecutives zeroes array
        self.conseq_zero = np.zeros(len(self.data))
        # Spaces between movements array
        self.spaces = np.zeros(len(self.data))
        # Parts counter analyzing rest periods
        self.cycle_counter = np.ones(len(self.data))
        
    def treat_data(self):    
        # Removing offset
        for i in self.data.index:
            self.data.at[i,'acc_1_x'] = self.data.iloc[i]['acc_1_x'] + self.data_offset
        # Zeroing values under the threshold
        for i in self.data.index:
            if self.data.iloc[i]['acc_1_x'] < self.threshold and self.data.iloc[i]['acc_1_x'] > - self.threshold:
                self.data.at[i, 'acc_1_x'] = 0
                self.conseq_zero[i] = self.conseq_zero[i-1] + 1

    def separate_by_zeros(self):
        # Get indexes
        index_threshold_zeros = np.where(self.conseq_zero==self.threshold_zeros)
        index_threshold_zeros = index_threshold_zeros[0]
        # Creating spaces array, where movement is 0 and rest is 1. Controlled by threshold_zeros number
        for i in index_threshold_zeros:
            ii = i
            while self.conseq_zero[ii] >= self.threshold_zeros:
                self.spaces[ii] = 1
                ii += 1
                if ii == self.conseq_zero.size:
                    break 
            ii = i-1
            while self.conseq_zero[ii] == self.conseq_zero[ii + 1] - 1:
                self.spaces[ii] = 1
                ii -= 1
                if ii == -1:
                    break

    def define_cycles(self):
        counter = 0
        self.flag = True
        #Define the cycle for every row in Dataframe 
        for i in range(0, len(self.spaces)):
            if self.spaces[i] == 0 and flag == False:
                counter += 1
                self.cycle_counter[i] = counter
                flag = True
            elif self.spaces[i] == 1:
                self.cycle_counter[i] = counter
                flag = False

    def flag_rest(self):
        #Add 'cycle_nr' and 'is_resting' arrays to Results Dataframe 
        self.data_rest_flagged = self.data
        self.data_rest_flagged.insert(1, "is_resting", self.spaces)
        self.data_rest_flagged.insert(2, "cycle_nr", self.cycle_counter)

    def get_results(self):
        engine = create_engine('mysql+pymysql://ipk:fraunhoferipk@192.168.137.1/arduino')
        #Creating Results Dataframe to be further added in Database
        self.results = pd.DataFrame(columns=['cycle_nr', 'cycle_ambient_temperature', 'cycle_ambient_humidity', 'cycle_cavity_temperature', 
                                        'cycle_cavity_pressure', 'cycle_closing_force'])
        #cycle_ambient_temperature  -- all the time
        #cycle_ambient_humidity     -- all the time
        #cycle_cavity_temperature   -- while closed
        #cycle_cavity_pressure      -- while closed
        #cycle_closing_force        -- while closed

        self.cycle_ambient_temperature = 0
        self.cycle_ambient_humidity = 0
        self.cycle_cavity_temperature = 0
        #self.cycle_cavity_pressure = 0
        #self.cycle_closing_force = 0

        #self.mean_ambient_temperature = 0
        #self.mean_ambient_humidity = 0
        #self.mean_cavity_temperature = 0
        #self.mean_cavity_pressure = 0
        #self.mean_closing_force = 0

        #Define first and last cycle
        cycle = self.data_rest_flagged.at[0, 'cycle_nr']
        last_cycle = self.data_rest_flagged.at[len(self.data_rest_flagged) - 1, 'cycle_nr']

        #Go through every cycle and calculate mean for all variables
        while cycle <= last_cycle:
            array_ambient_temperature = self.data_rest_flagged.loc[self.data_rest_flagged['cycle_nr'] == cycle].loc[:, 'lastTemp']
            if len(array_ambient_temperature) == 0:
                array_ambient_temperature = [0]
            array_ambient_humidity = self.data_rest_flagged.loc[self.data_rest_flagged['cycle_nr'] == cycle].loc[:, 'lastHum']
            if len(array_ambient_humidity) == 0:
                array_ambient_humidity = [0]
            array_cavity_temperature = self.data_rest_flagged.loc[(self.data_rest_flagged['cycle_nr'] == cycle) & (self.data_rest_flagged['is_resting'] == 0)].loc[:, 'tempKistler1']
            if len(array_cavity_temperature) == 0:
                array_cavity_temperature = [0]
            #array_cavity_pressure = self.data_rest_flagged.loc[[(self.data_rest_flagged['cycle_nr'] == cycle) & (self.data_rest_flagged['is_resting'] == 0)], ['']]
            #array_closing_force = self.data_rest_flagged.loc[[(self.data_rest_flagged['cycle_nr'] == cycle) & (self.data_rest_flagged['is_resting'] == 0)], ['']]
            
            #Define a dictionary with the values for a cycle
            new_row = {'cycle_nr':cycle, 
                       'cycle_ambient_temperature':mean(array_ambient_temperature),
                       'cycle_ambient_humidity':mean(array_ambient_humidity),
                       'cycle_cavity_temperature':mean(array_cavity_temperature),
                       'cycle_cavity_pressure':0,
                       'cycle_closing_force':0}
            
            #Insert dictionary in Dataframe
            self.results.loc[len(self.results)] = new_row
            
            cycle += 1

        print(self.results)
        # if_exists='replace' will replace the table if it already exists. You can change it to 'append' if you want to add rows to an existing table.
        self.results.to_sql(name='sql_results', con=engine, if_exists='replace', index=False) 

op = Operator()
op.get_data('TEST 15 PARTS')
print(op.data)
# PLOT RAW DATA
plt.plot(op.data.iloc[:]['ID'].to_numpy(), op.data.iloc[:]['acc_1_x'].to_numpy(), 'k')
op.treat_data()
op.separate_by_zeros()
op.define_cycles()

# Print parts number
print("NUMBER OF SPACES: " + str(op.cycle_counter[-1]/2))

op.flag_rest()

print(op.data_rest_flagged)

op.get_results()

# PLOT SPACES
plt.plot(op.data.iloc[:]['ID'].to_numpy(), op.spaces, 'c')
# PLOT FILTERED DATA
#plt.plot(op.data.iloc[:]['ID'].to_numpy(), op.data.iloc[:]['acc_1_x'].to_numpy(), 'r')
# PLOT ZEROS COUNTER
#plt.plot(op.data.iloc[:]['ID'].to_numpy(), op.conseq_zero, 'b', lw = 0.2)

plt.xlabel('Samples')
plt.ylabel('m/s')
plt.show()