import serial
import matplotlib.pyplot as plt



ser = serial.Serial('COM10', 115200) # <------ remember to change the port according to yours
class acc_reader():

    def read_acceleration(self):
        # self.x_accel = []
        while True:
            line = ser.readline()  # Recebe os bytes diretamente
            try:
                values = line.decode('latin-1').strip().split()
                if len(values) == 3:
                    self.x_accel = float(values[0])
                    return self.x_accel
            except UnicodeDecodeError:
                pass  # Ignora os bytes que não podem ser decodificados
try:
    acc = acc_reader()
    data_acc = []
    x = []

    while True:
        print(acc.read_acceleration())
        data_acc.append(acc.read_acceleration())
    
        

    
except KeyboardInterrupt:
    ser.close()
    for i in range(0, len(data_acc)):
            x.append(i)

plt.plot(x, data_acc)
plt.xlabel('Samples')
plt.ylabel('m/s')
plt.show()
