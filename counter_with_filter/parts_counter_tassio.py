import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path = {
    'TEST 3 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-1-3PARTS-07-12-2023.csv',
    'TEST 10 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-3-10PARTS-07-12-2023.csv',
    'TEST 12 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-4-12PARTS-07-12-2023.csv',
    'TEST 15 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-2-15PARTS-07-12-2023.csv'    
}

# Read CSV
data = pd.read_csv(data_path['TEST 15 PARTS'], sep=";", header=0, decimal=',')
# Invert Index
data = data[::-1].reset_index(drop=True)

# Offset seen on raw data
data_offset = - 0.3
# Threshold for zeroing values
threshold = 0.6
# How many zeros in a row is considered a pause
threshold_zeros = 33
# Consecutives zeroes array
conseq_zero = np.zeros(data.index[-1] + 1)
# Spaces between movements array
spaces = np.zeros(data.index[-1] + 1)

# Parts counter analyzing rest periods
parts_counter = 0
# Flag for counting
flag = False

print(data)

# Removing offset
for i in data.index:
    data.at[i,'acc_1_x'] = data.iloc[i]['acc_1_x'] + data_offset

# PLOT RAW DATA
plt.plot(data.iloc[:]['ID'].to_numpy(), data.iloc[:]['acc_1_x'].to_numpy(), 'k')

# Zeroing values under the threshold
for i in data.index:
    if data.iloc[i]['acc_1_x'] < threshold and data.iloc[i]['acc_1_x'] > -threshold:
        data.at[i, 'acc_1_x'] = 0
        conseq_zero[i] = conseq_zero[i-1] + 1

# Get indexes
index_threshold_zeros = np.where(conseq_zero==threshold_zeros)
index_threshold_zeros = index_threshold_zeros[0]

# Creating spaces array, where movement is 0 and rest is 1. Controlled by threshold_zeros number
for i in index_threshold_zeros:
    ii = i
    while conseq_zero[ii] >= threshold_zeros:
        print(ii)
        spaces[ii] = 1
        ii += 1
        if ii == conseq_zero.size:
            break 
    ii = i-1
    while conseq_zero[ii] == conseq_zero[ii + 1] - 1:
        spaces[ii] = 1
        ii -= 1
        if ii == -1:
            break 

# Counting parts
for i in spaces:
    if i == 0 and flag == False:
        parts_counter += 1
        flag = True
    elif i == 1:
        flag = False

# Print parts number
print("NUMBER OF SPACES: " + str(parts_counter/2))

# PLOT SPACES
plt.plot(data.iloc[:]['ID'].to_numpy(), spaces, 'c')
# PLOT FILTERED DATA
#plt.plot(data.iloc[:]['ID'].to_numpy(), data.iloc[:]['acc_1_x'].to_numpy(), 'r')
# PLOT ZEROS COUNTER
#plt.plot(data.iloc[:]['ID'].to_numpy(), conseq_zero, 'b', lw = 0.2)

plt.xlabel('Samples')
plt.ylabel('m/s')
plt.show()


