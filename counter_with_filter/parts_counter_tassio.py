import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path = {
    'TEST 3 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-1-3PARTS-07-12-2023.csv',
    'TEST 10 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-3-10PARTS-07-12-2023.csv',
    'TEST 12 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-4-12PARTS-07-12-2023.csv',
    'TEST 15 PARTS' : 'C:\\Users\\tassi\\GITHUB\\Smartool\\data\\TEST-2-15PARTS-07-12-2023.csv'    
}

data = pd.read_csv(data_path['TEST 10 PARTS'], sep=";", header=0, decimal=',')

data = data[::-1].reset_index(drop=True)

threshold = 0.5

conseq_zero = np.zeros(data.index[-1] + 1)

print(data)

for i in data.index:
    if data.iloc[i]['acc_1_x'] < threshold and data.iloc[i]['acc_1_x'] > -threshold:
        data.at[i, 'acc_1_x'] = 0
        conseq_zero[i] = conseq_zero[i-1] + 1

print(np.flip(data.iloc[:]['ID'].to_numpy()))
print(np.flip(data.iloc[:]['acc_1_x'].to_numpy()))
print(conseq_zero)

plt.plot(data.iloc[:]['ID'].to_numpy(), data.iloc[:]['acc_1_x'].to_numpy(), 'r')
plt.plot(data.iloc[:]['ID'].to_numpy(), conseq_zero, 'b')
plt.xlabel('Samples')
plt.ylabel('m/s')
plt.show()
