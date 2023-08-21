import time

start_time = time.time()

for i in range(0, 9, 1):
    print(i)

end_time = time.time()

tempo = end_time - start_time

print(f"O tempo do codigo foi {tempo}")