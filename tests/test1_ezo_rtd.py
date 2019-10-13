import machine
import time
import ezo_rtd


i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
atlas = ezo_rtd.EZO_RTD_I2C(i2c)
scales = ['kelvin', 'fahrenheit', 'celcius']
for scale in scales:
    atlas.set_scale(scale)
    print("EZO-RTD: Temperature Scale = {}  Temperature = {:0.3f}".format(atlas.set_scale('?'), atlas.take_reading()))
    


