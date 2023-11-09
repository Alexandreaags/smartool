import serial
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pymysql
import pandas as pd

#ser = serial.Serial('COM13', 115200) # <------ remember to change the port according to yours
sqlEngine       = create_engine('mysql+pymysql://ipk:fraunhoferipk@192.168.137.1', pool_recycle=3600)
dbConnection    = sqlEngine.connect()
frame           = pd.read_sql("select ID, data_4 from arduino.sql_data WHERE ID > 2230 ", dbConnection)

accel_threshold = 1 # Threshold of the acceleration 


class acc_reader():

    def read_acceleration(self):
        return frame['data_4'] + 9.7
         

try:
    acc = acc_reader()
    part_count = 0
    part_detected = False #Flag to count the part only one time
    # data_acc = []
    # x = []
    data = acc.read_acceleration()
    print(data)
    for i in data:
        print("Running...")
        # data_acc.append(acc.read_acceleration())
        
        if i > accel_threshold and not part_detected:
            print("Changing of position detected in X axis!")
            part_detected = True
            part_count += 1  # counts the parts
        
        if i < accel_threshold:
            part_detected = False  # Redefine to False when the position is less than threshold 
    part_count = part_count/2
    print(part_count*2)   
except KeyboardInterrupt:
    # ser.close()
    
    dbConnection.close()
    # for i in range(0, len(data_acc)):
    #         x.append(i)
    # print("Amount of manufactured parts:", part_count/2)

    # plt.plot(x, data_acc)
    # plt.xlabel('Samples')
    # plt.ylabel('m/s')
    # plt.show()
