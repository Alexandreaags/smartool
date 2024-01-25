from sqlalchemy import create_engine
import pandas as pd
import random as rd
from time import sleep

sqlEngine       = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
dbConnection    = sqlEngine.connect()

cycle_nr = 1

while(1):
    mean_ambient_temperature = rd.randrange(19, 35, 1)
    mean_ambient_humidity = rd.randrange(1, 99, 1)
    mean_cavity_temperature = rd.randrange(0, 200, 1)
    mean_cavity_pressure = rd.randrange(0, 1000, 1)
    mean_closing_force = rd.randrange(0, 350000, 1)
    initial_time = 2
    final_time = 4

    frame_2 = pd.DataFrame(data = [[cycle_nr, mean_ambient_temperature, mean_ambient_humidity, mean_cavity_temperature, 
                                    mean_cavity_pressure, mean_closing_force, initial_time, final_time]], columns = ['cycle_nr', 'mean_ambient_temperature', 
                                                       'mean_ambient_humidity', 'mean_cavity_temperature', 
                                                       'mean_cavity_pressure', 'mean_closing_force', 
                                                       'initial_time', 'final_time'])
    print(frame_2)
    cycle_nr += 1

    frame_2.to_sql('sql_results', index=False, con=dbConnection, schema='arduino', if_exists='append')
    sleep(0.2)

dbConnection.close()
    
