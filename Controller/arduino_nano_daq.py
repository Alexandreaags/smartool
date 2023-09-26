import serial
from time import sleep

class Device():
    DEFAULTS = {
        'write_termination': '\n',
        'read_termination': '\n',
        'encoding': 'utf-8',
        'baudrate': 115200,
        'read_timeout': 1,
        'write_timeout': 1
        }

    def __init__(self, port):
        self.port = port
        self.rsc = None
        self.serial_number = None

    def initialize(self):
        self.rsc = serial.Serial(port=self.port,
                                 baudrate=self.DEFAULTS['baudrate'],
                                 timeout=self.DEFAULTS['read_timeout'],
                                 write_timeout=self.DEFAULTS['write_timeout'])
        sleep(1)

    def get_serial_message(self):
        self.rsc.flushInput()
        line = self.rsc.readline()  # Recebe os bytes diretamente
        values = line.decode('latin-1').strip().split()
        if len(values) > 0 and values[0] == 'A':
            return values
        else:
            return self.get_serial_message()

    def finalize(self):
        if self.rsc is not None:
            self.rsc.close()


if __name__ == '__main__':
    dev = Device('COM13')
    dev.initialize()
    
    print(dev.get_serial_message())

    dev.finalize()