import serial

ser = serial.Serial('COM10', 9600)

while True:
    line = ser.readline()
    # print(line)
    try:
        values = line.decode().strip()
        print(values)
    except UnicodeDecodeError:
        pass  # Ignora os bytes que não podem ser decodificados