import serial
import matplotlib.pyplot as plt
import pandas as pd

data_path = {
    'TEST 3 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-1-3PARTS-07-12-2023.csv',
    'TEST 10 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-3-10PARTS-07-12-2023.csv',
    'TEST 12 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-4-12PARTS-07-12-2023.csv',
    'TEST 15 PARTS' : 'C:/Users/Alexa/Programs/Smartool/data/TEST-2-15PARTS-07-12-2023.csv'    
}

data = pd.read_csv(data_path['TEST 10 PARTS'], sep=";", header=0, decimal=',')


accel_threshold = 2.1 # Threshold of the acceleration 



data_acc = []
part_count = 0
part_detected = False #Flag to count the part only one time
    
# print("Running...")
        
        
data_acc.append(data['acc_1_x'])
# print(data_acc)
last_datas = data_acc[-30:]# separe only the last datas from the list
sum_data = sum(last_datas)# sum the last 100 datas 
mean_data = sum_data/len(last_datas)# mean of the last 100 datas
print(mean_data)

if mean_data > accel_threshold and not part_detected:

    print("Changing of position detected in X axis!")
    part_detected = True
    part_count += 1  # Incrementa a contagem de peças
        
if mean_data < accel_threshold:
    part_detected = False  # Redefine para Falso quando a posição volta ao normal

    print("Amount of manufactured parts:", part_count)
    # print(data_acc)
    