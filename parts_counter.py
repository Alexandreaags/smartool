import serial
from time import sleep

ser = serial.Serial('COM6', 115200)

# Limite de aceleração para considerar como produção de peça
# acel_limit = 9.0  # Ajuste este valor conforme necessário
# piece_count = 0
# accel_values = []
# prev_x_accel = 0.0
# accel_threshold = 0.5 
try:
    while True:
        line = ser.readline().decode()
        # print(line)
        values = line.strip().split()
        if len(values) == 3:
            x_accel = float(values[0])
            # y_accel = float(values[1])
            # z_accel = float(values[2])
            print(x_accel)#, y_accel, z_accel)
            #sleep(.5)
            #accel_values.append([x_accel, y_accel, z_accel])
            # x_accel_change = abs(x_accel - prev_x_accel)
            # if x_accel_change > accel_threshold:
            #     piece_count += 1
            #     sleep(1)
            #     print("Piece manufactured!")
            # prev_x_accel = x_accel
        # print(line[16:-6])
        # x_accel = float(line[2:-15])
        # y_accel = float(line[-15:-7])
        # z_accel = float(line[-7:-1])
        # print(x_accel, y_accel, z_accel)
        # accel_values.append([x_accel, y_accel, z_accel])
            
            # if x_accel > acel_limit:
            #     piece_count += 1
            #     print("Peça produzida! Total de peças:", piece_count)
        
except KeyboardInterrupt:
    #print(f"{piece_count} pieces was manufactured!!")
    ser.close()
