#from Smartool.Controller.arduino_nano_daq import Device
from Smartool.Controller.dummy_daq import Device
import yaml
import os
import threading
from time import sleep
from Smartool import ur
import numpy as np

class ArduinoNano():
    def __init__(self, config_file):
        self.config_file = config_file
        self.is_running = False #Variable to check if the scan is running
        self.keep_running = False
        self.scan_range = [0]
        self.scan_data = [0]

    def load_config(self):
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

    def acc_scan(self):
        if self.is_running == True:
            print('Scan already running!')
            return
        self.is_running = True
        
        delay = ur(self.config['Scan']['delay'])
        num_steps = int(self.config['Scan']['num_steps'])
        self.scan_data = np.zeros(num_steps) * ur('m/s²')
        self.scan_range = np.linspace(0, num_steps-1, num_steps)

        i = 0
        counter = 0
        
        self.keep_running = True
        try:
            while True:
                if not self.keep_running:
                    break
                if counter < num_steps:
                    message = self.daq.get_serial_message()[0] * ur('m/s²')
                    self.scan_data[i] = message
                    counter += 1
                    i += 1
                    print(counter)
                    print("         ")
                    print(self.scan_data)
                    print("         ")
                    print(len(self.scan_data))
                    sleep(delay.m_as('s'))
                else:
                    print("ENTROUUUU")
                    message = self.daq.get_serial_message()[0] * ur('m/s²')
                    self.scan_data = np.append(self.scan_data, message)
                    self.scan_data = self.scan_data[1:]
                    i += 1
                    #print(message)
                    print("         ")
                    print(self.scan_data)
                    sleep(delay.m_as('s'))
        except KeyboardInterrupt:
            self.is_running = False
            self.keep_running = False
            return
        self.is_running = False

    def start_scan(self):
        self.scan_thread = threading.Thread(target=self.acc_scan)
        self.scan_thread.start()

    def stop_scan(self):
        self.keep_running = False

    def finalize(self):
        print('Finalizing Experiment')
        self.stop_scan()
        while self.is_running:
            sleep(.1)
        self.daq.finalize()