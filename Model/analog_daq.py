from PythonForTheLab.Controller.pftl_daq import Device
from PythonForTheLab.Controller.base_daq import DAQBase

from PythonForTheLab import ur

class AnalogDaq(DAQBase):
    def __init__(self, port):
        self.port = port
        self.driver = Device(self.port)

    def __str__(self):
        return 'Analog DAQ'

    def initialize(self):
        self.driver.initialize()
        self.set_voltage(0,ur('0V'))
        self.set_voltage(1,ur('0V'))
                    
    def get_voltage(self, channel):
        voltage_bits = self.driver.get_analog_input('CH' + str(channel))
        voltage = voltage_bits*ur('3.3V')/1023
        return voltage

    def set_voltage(self, channel, volts):
        voltage_bits = round(volts.m_as('V')/3.3*4095)
        self.driver.set_analog_value('CH' + str(channel), voltage_bits)

    def finalize(self):
        self.set_voltage(0,ur('0V'))
        self.set_voltage(1,ur('0V'))
        self.driver.finalize()

if __name__ == '__main__':
    daq = AnalogDaq('COM11')
    daq.initialize()
    voltage = ur('3000mV')
    daq.set_voltage(0,voltage)
    input_volts = daq.get_voltage(0)
    print(input_volts)
    daq.finalize()
        