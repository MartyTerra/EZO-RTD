"""
This MicroPython module implements an interface to the Atalas Scientific 
EZO-RTD Interface Board.

Reading:    temperature         Data type           floating point
Units:      C, K, or F          Decimal places:     3
Encoding:   ASCII               Smallest string:    4 chars
Format      string              Largest string      40 chars

Datasheet: ???
"""
import machine
import array
import time


DEVICE_NAME = 'EZO_RTD'

EZO_RTD_I2C_DEFAULT_ADDRESS = const(0x66)
EZO_RTD_I2C_ADDRESS         = EZO_RTD_I2C_DEFAULT_ADDRESS

RSP_NO_DATA    = const(0xFF)
RSP_NOT_READY  = const(0xFE)
RSP_SUCCESS    = const(0x01)    
RSP_ERROR      = const(0x02)

CMD_BAUD    = b'Baud'       # switch back to UART mode
CMD_CAL     = b'Cal'        # performs calibration       
CMD_BAUD    = b'D'          # enable/disable data logger
CMD_EXPORT  = b'Export'     # export calibration
CMD_FACTORY = b'Factory'    # enable factory reset
CMD_FIND    = b'Find'       # finds devices with white blinking LED
CMD_I       = b'i'          # device information
CMD_I2C     = b'I2C'        # changed I2C address
CMD_IMPORT  = b'Import'     # import calibration
CMD_L       = b'L'          # enable/disable LED
CMD_M       = b'M'          # memory recall/clear
CMD_PLOCK   = b'Plock'      # enable/disable protocol lock
CMD_R       = b'R'          # returns a single reading
CMD_S       = b'S'          # temperature scale (C, K, F)
CMD_SLEEP   = b'Sleep'      # enter sleep mode/low power
CMD_STATUS  = b'Status'     # retrieve status inforamtion


class EZO_RTD:
    def __init__(self):
        """
        self._write(CMD_S+',c') # set units to Celcius
        time.sleep(1)
        """
        self.set_scale('celcius')
        if self.self_test() is False:
            print("ERROR: EZO-RTD falied self test")

    def self_test(self):
        pass

    @property
    def kelvin(self):
        return (self.celcius + 273.15)
    @property
    def fahrenheit(self):
        return (self.celcius * (9.0/5.0) + 32)
    @property
    def celcius(self):
        return self.take_reading()

    def set_scale(self, scale):
        scales = {  'celcius':      CMD_S+',c',
                    'kelvin':       CMD_S+',k',
                    'fahrenheit':   CMD_S+',f',
                    '?':            CMD_S+',?'}
        if scale not in list(scales.keys()):
            print("{}: error, wrong scale option: {}".format(DEVICE_NAME, scale))
        self._write(scales[scale])
        time.sleep(0.5)
        if scale is '?':
            data = self._read(6)
            response, t_c, null = data[0], data[1:5], data[5]
            time.sleep(1)            

    def take_reading(self):
        t_c = self.command_write_read(CMD_R, 0.7, 8)
        time.sleep(1)
        return float(t_c)

    def device_info(self):
        data = self.command_write_read(CMD_I, 0.5, 13)
        (rsp, device, firmware) = data.split(',')
        return

    def command_write_read(self, cmd, delay, n):
        self._write(cmd)
        time.sleep(delay)
        data = self._read(n)
        rsp, payload, null = data[0], data[1:n], data[n]
        return payload

    # Low Level, Private methods
    def _write(self, data):
        raise NotImplementedError()
    def _read(self, n):
        raise NotImplementedError()


class EZO_RTD_I2C(EZO_RTD):
    def __init__(self, i2c, address=EZO_RTD_I2C_ADDRESS, name=DEVICE_NAME):
        self.i2c = i2c
        self.address = address
        self.name = name
        print("%s address = 0x%02x" % (self.name, self.address))
        super().__init__()

    # Low Level, Private methods
    #
    def _write(self, data):
        self.i2c.writeto(self.address, data)
    
    def _read(self, n):
        return self.i2c.readfrom(self.address, n)


"""
SELF TEST
"""
def self_test():
    print("MSG: Start of Atlas Scientific EZO-RTD self test")
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
    atlas = EZO_RTD_I2C(i2c)
    while True:
        print(atlas.celcius)
    print("MSG: End of Atlas Scientific EZO-RTD self test")

self_test()

