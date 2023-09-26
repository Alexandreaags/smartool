from Smartool.Controller.arduino_nano_daq import Device        #USE THIS FOR REAL ARDUINO AND ACCELEROMETER
#from Smartool.Controller.dummy_daq import Device                #USE THIS FOR TESTING
import yaml
import threading
from time import sleep
from Smartool import ur
import numpy as np


### 
### ADDRESSING OF VARIABLES IN GET.SERIAL.MESSAGE ARRAY
### [0] = 'A' // CHARACTER USED TO KNOW WHEN A LINE STARTS ON TERMINAL
### [1] = ACC_LIS3DH X AXIS // M/S²
### [2] = ACC_LIS3DH Y AXIS // M/S²
### [3] = ACC_LIS3DH Z AXIS // M/S²
### [4] = ACC_MPU6050 X AXIS // M/S²
### [5] = ACC_MPU6050 Y AXIS // M/S²
### [6] = ACC_MPU6050 Z AXIS // M/S²
### [7] = DHT22 TEMPERATURE // °C
### [8] = DHT22 HUMIDITY // %
### 



class ArduinoNano():
    def __init__(self, config_file):
        self.config_file = config_file                          #File used to set scan settings
        self.is_running = False                                 #Variable to check if the scan is running
        self.keep_running = False                               #Variable used to permit or not the continuing of the scan, inputed by user
        self.scan_range = [0]                                   #Number of samples
        self.scan_data = [0]
        self.delay = ''
        self.num_steps = 0                                    #Data of scan
        self.sensor = {
            "Acc. LIS3DH" : self.acc_scan_LIS3DH,
            "Acc. MPU6050" : self.acc_scan_MPU6050,
            "Temp. DHT22" : self.term_scan_temp_DHT22,
            "Hum. DHT22" : self.term_scan_hum_DHT22
        }
        self.data_unit = ''
        self.data_unit_label = ''
        self.data_index = 0

    def load_config(self):                                      #Module used to open and verify config file
        with open (self.config_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.config = data
        number_err = 0
        for k in self.config:
            for i in self.config[k]:
                if self.config[k][i] == None:
                    number_err = number_err + 1
        if number_err > 1:
            print(10*'-')
            print('WARNING: THERE ARE ' + str(number_err) + ' PARAMETERS WITHOUT VALUES IN CONFIGURATION FILE.')
            print(10*'-')
        elif number_err == 1:
            print(10*'-')
            print('WARNING: THERE IS ONE PARAMETER WITHOUT VALUE IN CONFIGURATION FILE.')
            print(10*'-')

    def load_daq(self):
        self.daq = Device(self.config['DAQ']['port'])
        self.daq.initialize()

    def scan(self):
        if self.is_running == True:
            print('Scan already running!')
            return
        self.is_running = True
        
        self.delay = ur(self.config['Scan']['delay'])
        self.num_steps = int(self.config['Scan']['num_steps'])
        self.scan_data = np.zeros(self.num_steps) * ur(self.data_unit)
        self.scan_range = np.linspace(0, self.num_steps-1, self.num_steps)

        counter = 0
        
        self.keep_running = True            
        try:
            while True:
                if not self.keep_running:   
                    break
                if counter < self.num_steps:     #getting array of acceleration until values are atributed to all elements of the array
                    message = float(self.daq.get_serial_message()[self.data_index]) * ur(self.data_unit)
                    self.scan_data[counter] = message
                    counter += 1
                    sleep(self.delay.m_as('s'))
                else:                       #when array is full, append a new element, remove the first one and rearrange the positions
                    message = float(self.daq.get_serial_message()[self.data_index]) * ur(self.data_unit)
                    self.scan_data = np.append(self.scan_data, message)
                    self.scan_data = self.scan_data[1:]
                    sleep(self.delay.m_as('s'))
        except KeyboardInterrupt:
            self.is_running = False
            self.keep_running = False
            return
        self.is_running = False

    def acc_scan_LIS3DH(self):                                         #Scan module used for accelerometer LIS3DH
        self.data_index = 1
        self.data_unit = 'm/s²'
        self.data_unit_label = 'm/s²'
        self.scan()

    def acc_scan_MPU6050(self):                                         #Scan module used for accelerometer MPU6050
        self.data_index = 4
        self.data_unit = 'm/s²'
        self.data_unit_label = 'm/s²'
        self.scan()

    def term_scan_temp_DHT22(self):
        self.data_index = 7
        self.data_unit = 'delta_degree_Celsius'
        self.data_unit_label = '°C'
        self.scan()

    def term_scan_hum_DHT22(self):
        self.data_index = 8
        self.data_unit = 'dimensionless'
        self.data_unit_label = '%'
        self.scan()

    def start_scan(self, sensor_name):
        self.scan_thread = threading.Thread(target=self.sensor[sensor_name])
        self.scan_thread.start()

    def stop_scan(self):
        self.keep_running = False

    def finalize(self):
        print('Finalizing Experiment')
        self.stop_scan()
        while self.is_running:
            sleep(.1)
        self.daq.finalize()