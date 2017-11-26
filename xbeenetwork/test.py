from sensornet import SensorNet
from time import sleep
import logging, sys
def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}:{1}".format(str(value), tb.print_tb()))

logging.basicConfig()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
sys.excepthook = my_handler
x = SensorNet('/dev/cu.usbserial-DN018RGN')
sleep(2)
y=x.units['ROUTER1']
