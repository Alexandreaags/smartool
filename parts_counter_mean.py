import serial



ser = serial.Serial('COM13', 115200) # <------ remember to change the port according to yours


accel_threshold = 6 # Threshold of the acceleration 


class acc_reader():

    def read_acceleration(self):
        # self.x_accel = []
        while True:
            line = ser.readline()  # Recebe os bytes diretamente
            try:
                values = line.decode('latin-1').strip().split()
                if len(values) == 3:
                    self.x_accel = float(values[0])
                    return self.x_accel + 9.58
            except UnicodeDecodeError:
                pass  # Ignora os bytes que não podem ser decodificados

try:
    acc = acc_reader()
    data_acc = []
    part_count = 0
    part_detected = False #Flag to count the part only one time

    while True:
        # print("Running...")
        
        
        data_acc.append(acc.read_acceleration())
        # print(data_acc)
        last_datas = data_acc[-30:]# separe only the last datas from the list
        sum_data = sum(last_datas)# sum the last 100 datas 
        mean_data = sum_data/len(last_datas)# mean of the last 100 datas
        print(mean_data)

        if mean_data > accel_threshold and not part_detected:

            print("Changing of position detected in X axis!")
            part_detected = True
            part_count += 1  # Incrementa a contagem de peças
        
        if mean_data < accel_threshold:
            part_detected = False  # Redefine para Falso quando a posição volta ao normal

except KeyboardInterrupt:
    ser.close()
    print("Amount of manufactured parts:", part_count)
    # print(data_acc)
    