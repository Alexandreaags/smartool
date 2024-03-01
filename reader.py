import serial
import time

ser = serial.Serial('COM3', 115200) # <------ remember to change the port according to yours


x_accel = []
while True:
    line = ser.readline()  # Recebe os bytes diretamente
    try:
        values = line.decode('latin-1').strip().split()
        if len(values) == 3:
            x_accel = float(values[0])
            print(x_accel)
    except UnicodeDecodeError:
        pass  # Ignora os bytes que não podem ser decodificados