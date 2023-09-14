import threading
import os
from datetime import datetime
import yaml
import numpy as np
from time import sleep
from PythonForTheLab.Model.analog_daq import AnalogDaq
from PythonForTheLab import ur

class Experiment():
    def __init__(self, config_file):    #LED blinking on and off    
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
        self.daq = AnalogDaq(self.config['DAQ']['port'])
        self.daq.initialize()

    def do_scan(self):
        if self.is_running == True:
            print('Scan already running!')
            return
        self.is_running = True
        start = ur(self.config['Scan']['start']).m_as('V')
        stop = ur(self.config['Scan']['stop']).m_as('V')
        resistance = ur(self.config['Scan']['resistance'])
        num_steps = int(self.config['Scan']['num_steps'])
        delay = ur(self.config['Scan']['delay'])
        self.scan_range = np.linspace(start, stop, num_steps) * ur('V')
        self.scan_data = np.zeros(num_steps) * ur('mA')
        i = 0
        self.keep_running = True
        try:
            for volt in self.scan_range:
                if not self.keep_running:
                    break
                self.daq.set_voltage(self.config['Scan']['channel_out'], volt)
                measured_voltage = self.daq.get_voltage(self.config['Scan']['channel_in'])
                self.scan_data[i] = measured_voltage/resistance
                i += 1
                sleep(delay.m_as('s'))
        except KeyboardInterrupt:
            self.is_running = False
            self.keep_running = False
            return
        self.is_running = False

    def save_data(self):
        data_folder = self.config['Saving']['folder']   #set the folder for the experiment to be saved, based on the config file
        today_folder = f'{datetime.today():%Y-%m-%d}'   #set the name for the folder of the day
        saving_folder = os.path.join(data_folder, today_folder) #put the path of the today folder in the data folder
        if not os.path.isdir(saving_folder):    #if there is no today folder yet, create one
            os.makedirs(saving_folder)

        row1 = []
        row2 = []

        for i in range(len(self.scan_range)):
            row1.append(self.scan_range[i].m_as('V'))
        for i in range(len(self.scan_data)):
            row2.append(self.scan_data[i].m_as('mA'))


        data = np.vstack([row1,row2]).T #creates an array with the two other arrays in two collumns

        #data = np.vstack([self.scan_range, self.scan_data]).T #creates an array with the two other arrays in two collumns
        header = "Scan range in 'V', Scan Data in 'mA'"  #header of the .bat file

        filename = self.config['Saving']['filename']    #filename of config file
        base_name = filename.split('.')[0]
        ext = filename.split('.')[-1]
        i = 1
        while os.path.isfile(os.path.join(saving_folder,f'{base_name}_{i:04d}.{ext}')):
            i += 1
        data_file = os.path.join(saving_folder, f'{base_name}_{i:04d}.{ext}')
        metadata_file = os.path.join(saving_folder,f'{base_name}_{i:04d}_metadata.yml')
        np.savetxt(data_file, data, header=header)
        with open(metadata_file, 'w') as f:
            f.write(yaml.dump(self.config, default_flow_style=False))

    def start_scan(self):
        self.scan_thread = threading.Thread(target=self.do_scan)
        self.scan_thread.start()

    def stop_scan(self):
        self.keep_running = False

    def finalize(self):
        print('Finalizing Experiment')
        self.stop_scan()
        while self.is_running:
            sleep(.1)
        self.daq.finalize()