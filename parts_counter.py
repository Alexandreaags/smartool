import serial
import matplotlib.pyplot as plt

ser = serial.Serial('COM13', 115200) # <------ remember to change the port according to yours


accel_threshold = 6 # Threshold of the acceleration 


class acc_reader():

    def read_acceleration(self):
        self.x_accel = []
        while True:
            line = ser.readline()  # Recebe os bytes diretamente
            try:
                values = line.decode('latin-1').strip().split() #strip remove blank spaces
                if len(values) == 3:
                    self.x_accel = float(values[0])
                    return self.x_accel + 9.58
            except UnicodeDecodeError:
                pass  # Ignora os bytes que não podem ser decodificados

try:
    acc = acc_reader()
    part_count = 0
    part_detected = False #Flag to count the part only one time
    data_acc = []
    x = []

    while True:
        print("Running...")
        data_acc.append(acc.read_acceleration())
        data = acc.read_acceleration()
        if data > accel_threshold and not part_detected:
            print("Changing of position detected in X axis!")
            part_detected = True
            part_count += 1  # counts the parts
        
        if data < accel_threshold:
            part_detected = False  # Redefine to False when the position is less than threshold 

except KeyboardInterrupt:
    ser.close()
    for i in range(0, len(data_acc)):
            x.append(i)
    print("Amount of manufactured parts:", part_count/2)

    plt.plot(x, data_acc)
    plt.xlabel('Samples')
    plt.ylabel('m/s')
    plt.show()
