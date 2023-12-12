import matplotlib.pyplot as plt
import pandas as pd

data_path = {
    'TEST 3 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-1-3PARTS-07-12-2023.csv',
    'TEST 10 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-3-10PARTS-07-12-2023.csv',
    'TEST 12 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-4-12PARTS-07-12-2023.csv',
    'TEST 15 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-2-15PARTS-07-12-2023.csv'    
}

data = pd.read_csv(data_path['TEST 10 PARTS'], sep=";", header=0, decimal=',')

data['date'] = pd.to_datetime(data['date'])
# Convert datetime64[ns] to seconds, ms, micros
data['date_ms'] = (data['date'] - pd.to_datetime('2023-12-07 16:13:43.667954')) // pd.Timedelta(milliseconds=1)
# data['date_s'] = (data['date'] - pd.to_datetime('2023-12-07 16:13:43.667954')) // pd.Timedelta(seconds=1)
# data['date_micros'] = (data['date'] - pd.to_datetime('2023-12-07 16:13:43.667954')) // pd.Timedelta(microseconds=1)
# print(data['date_seconds'])

# plt.figure(figsize=(10, 6))
plt.plot(data['date_ms'], data['acc_1_x'], label='X-axis')
plt.xlabel('Time(ms)')
plt.ylabel('Acceleration')
plt.title('Accelerometer Data over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()
    
