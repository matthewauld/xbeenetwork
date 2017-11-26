from sensornet import SensorNet
from time import sleep
import logging, sys
def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}:{1}".format(str(value), tb.print_tb()))


logger = logging.getLogger(__name__)

hdlr = logging.FileHandler('/var/tmp/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

sys.excepthook = my_handler
x = SensorNet('/dev/cu.usbserial-DN018RGN')
sleep(2)
y=x.units['ROUTER1']
