import serial
import time


ser = serial.Serial('COM6', 115200)

accel_interval = 2  # Intervalo de tempo em segundos para coletar dados de aceleração
accel_threshold = 2.7 # Ajuste este valor conforme necessário




class acc_reader():

    def read_acceleration(self):
        self.x_accel = []
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
    part_count = 0
    part_detected = False

    while True:
        print("Running...")
        
        data = acc.read_acceleration()
        if data > accel_threshold and not part_detected:
            print("Mudança de posição detectada no eixo X!")
            part_detected = True
            part_count += 1  # Incrementa a contagem de peças
        
        if data < accel_threshold:
            part_detected = False  # Redefine para False quando a posição volta ao normal

except KeyboardInterrupt:
    ser.close()
    print("Total de peças produzidas:", part_count)
