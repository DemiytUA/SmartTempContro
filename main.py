import gpiozero as gpio0
import os
import glob
import time

# import libraries



# Connection to the temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Opening a data file
def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()

# Temperature reading
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



heater_gpio = gpio0.LED(23)    # Heater relay control pin
heating = False  # Heater status flag


# Prompt user to set the temperature range
print("Enter the temperature range to maintain:")
min_temp = float(input("Minimum value: "))
max_temp = float(input("Maximum value: "))


heater_off_temp = max_temp

temps = [max_temp]      # list of temperature values
write_temp_to_list = False


print("\n\n")


while True:
    try:
        # getting temperature value
        temp_c = read_temp()
        print(f'Температура: {temp_c} °C')

        if write_temp_to_list:
            temps.append(temp_c)

        if temp_c <= min_temp and not heating:
            write_temp_to_list = True
            heater_off_temp = max_temp - ((max(temps) - max_temp) * (max_temp / max(temps)))

            # turning on the heater
            print("\nHEATER ON\n")
            heater_gpio.on()
            heating = True

        if temp_c >= heater_off_temp and heating:
            # turning off the heater
            print("\nHEATER OFF\n")
            heater_gpio.off()
            heating = False

        time.sleep(1)


    except Exception as e:
        print("Temperature reading error:", e)
        time.sleep(1)