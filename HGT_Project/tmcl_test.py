from serial import Serial
from time import sleep
import pyTMCL

MODULE_ADDRESS = 1

serial_port = Serial("/dev/ttyACM0")

bus = pyTMCL.connect(serial_port)

motor = bus.get_motor(MODULE_ADDRESS)

motor.rotate_left(1234)
sleep(2)
motor.stop()