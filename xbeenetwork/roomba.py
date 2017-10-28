from sensornet import SensorNet
import logging
import time
import sys


def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}:{1}".format(str(value), tb.print_tb()))

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sys.excepthook = my_handler

net = SensorNet('/dev/cu.usbserial-DN018RGN')
time.sleep(1)
car = net.units['ROUTER1']

while True:
    x = input(">")
    if x == 'w':
        car.move_forwards()
    elif x == 's':
        car.move_backwards()
    elif x == 'q':
        car.stop()
        break
    elif x == 'a':
        car.rotate_left()
    elif x == 'd':
        car.rotate_right()
    else:
        car.stop()
