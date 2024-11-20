import gpiozero as gpio0
import os
import glob
import time

# Підключення до сенсора
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c



heater_gpio = gpio0.LED(23)
heating = False



print("Напишіть діапазон, в якому треба підтримувати температуру")
min_t = float(input("Мінімальне значення: "))
max_t = float(input("Максимальне значення: "))


heater_off_temp = 0
temps = [max_t]
write_temp_to_list = False




print("\n\n")



while True:
    try:
        temp_c = read_temp()
        print(f'Температура: {temp_c} °C')
        time.sleep(1)


        if write_temp_to_list:
            temps.append(temp_c)




        if temp_c <= min_t and not heating:
            write_temp_to_list = True
            heater_off_temp = max_t - ((max(temps) - max_t) * (max_t / max(temps)))


            print(max(temps), max_t)
            print(heater_off_temp)



            print("\nHEATER ON\n")
            heater_gpio.on()
            heating = True
        if temp_c >= heater_off_temp and heating:
            print("\nHEATER OFF\n")
            heater_gpio.off()  # Закрити реле
            heating = False
    except Exception as e:
        print("Помилка читання температури:", e)
        time.sleep(1)
