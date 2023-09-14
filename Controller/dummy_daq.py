#dummy daq for testing the model and view
from time import sleep
import random as rd

class Device():
    def __init__(self, port):
        rd.seed()
        self.port = port
        self.rsc = None
        self.serial_number = None
        self.values = []

    def initialize(self):
        pass

    def get_serial_message(self):
        self.values = [round(rd.uniform(-5, 5), 2), round(rd.uniform(-5, 5), 2), round(rd.uniform(-5, 5), 2)]
        return self.values

    def finalize(self):
        if self.rsc is not None:
            self.rsc.close()


if __name__ == '__main__':
    dev = Device('COM13')
    dev.initialize()
    
    print(dev.get_serial_message())

    dev.finalize()