from sqlalchemy import create_engine
import pymysql
import pandas as pd

#ser = serial.Serial('COM13', 115200) # <------ remember to change the port according to yours
sqlEngine       = create_engine('mysql+pymysql://ipk:fraunhoferipk@192.168.137.1', pool_recycle=3600)
dbConnection    = sqlEngine.connect()
frame           = pd.read_sql("select ID, data_4 from arduino.sql_data WHERE ID > 0", dbConnection)
print(frame['data_4'])
print(type(frame['data_4']))
accel_threshold = 6 # Threshold of the acceleration 


class acc_reader():

    def read_acceleration(self):
        return frame['data_4'] + 9.58


    
acc = acc_reader()
data = []
data.append(acc.read_acceleration())
print(data)
# print(type(data))