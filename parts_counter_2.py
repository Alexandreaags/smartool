import serial
import time

ser = serial.Serial('COM6', 115200)

accel_interval = 2  # Intervalo de tempo em segundos para coletar dados de aceleração
accel_threshold = 1  # Ajuste este valor conforme necessário




class acc_reader():

    def read_acceleration(self):
        self.x_accel = []
        while True:
            line = ser.readline().decode()
            values = line.strip().split()
            if len(values) == 3:
                self.x_accel = float(values[0])
                #print(x_accel)
                # y_accel = float(values[1])
                # z_accel = float(values[2])
                return self.x_accel

try:
    acc = acc_reader()
    start_time = time.time()

    while True:
        print("Nada")
        
        #print(read_acceleration(x_accel), read_acceleration(y_accel), read_acceleration(z_accel))
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= accel_interval:
            for data in acc.read_acceleration():
                if data > accel_threshold:
                    print("Mudança de posição detectada no eixo X!")
                    acc.read_acceleration()
                    break
           
           
            # x_accel = read_acceleration()
            # x_accel_change = abs(x_accel - prev_x_accel)
            
            # if x_accel_change > accel_threshold:
                
            
        start_time = current_time
except KeyboardInterrupt:
    print(acc.read_acceleration())
    ser.close()
