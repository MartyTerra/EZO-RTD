import machine
import time
import ezo_rtd


print("MSG: Start of Atlas Scientific EZO-RTD self test")
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
atlas = ezo_rtd.EZO_RTD_I2C(i2c)
while True:
    print(atlas.celcius)
print("MSG: End of Atlas Scientific EZO-RTD self test")

