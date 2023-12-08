import serial
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pymysql
import pandas as pd

#ser = serial.Serial('COM13', 115200) # <------ remember to change the port according to yours
sqlEngine       = create_engine('mysql+pymysql://ipk:fraunhoferipk@192.168.137.1', pool_recycle=3600)
dbConnection    = sqlEngine.connect()
frame           = pd.read_sql("select ID, data_1 from arduino.sql_data WHERE ID > 0 ", dbConnection)

accel_threshold = 2.1 # Threshold of the acceleration 


class acc_reader():

    def read_acceleration(self):
        return frame['data_1'] - 0.35
    # def get_serial_message(self):
    #     #ser.flushInput()
    #     #line = ser.readline()  # Recebe os bytes diretamente
    #     values = line.decode('latin-1').strip().split()
    #     if len(values) > 0 and values[0] == 'A':
    #         return values
    #     else:
    #         return self.get_serial_message()

    # def read_acceleration(self):
    #     self.x_accel = []
    #     while True:
    #         line = ser.readline()  # Recebe os bytes diretamente
    #         try:
    #             values = line.decode('latin-1').strip().split() #strip remove blank spaces
    #             if len(values) == 3:
    #                 self.x_accel = float(values[0])
    #                 return self.x_accel + 9.58
    #         except UnicodeDecodeError:
    #             pass  # Ignora os bytes que não podem ser decodificados

try:
    acc = acc_reader()
    part_count = 0
    part_detected = False #Flag to count the part only one time
    data_acc = []
    x = []
    data = acc.read_acceleration()
    print(data)
    for i in data:
        print("Running...")
        print(i)
        data_acc.append(i)
        
        if i > accel_threshold and not part_detected:
            print("Changing of position detected in X axis!")
            part_detected = True
            part_count += 1  # counts the parts
        
        if i < accel_threshold:
            part_detected = False  # Redefine to False when the position is less than threshold 
    # part_count = part_count/2
    print(part_count)   
    # print(data)
    for i in range(0, len(data_acc)):
            x.append(i)
    print("Amount of manufactured parts:", part_count/2)

    plt.plot(x, data_acc)
    plt.xlabel('Samples')
    plt.ylabel('m/s')
    plt.show()
except KeyboardInterrupt:
    # ser.close()
    
    dbConnection.close()
    
