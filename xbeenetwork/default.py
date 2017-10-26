from xbeenetwork import SensorNet
import logging
import time


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
net = SensorNet('/dev/cu.usbserial-DN018RGN')


def stop():
    net.send_data('ROUTER1', [131])



def move_backwards():
    net.send_data('ROUTER1', [131])
    time.sleep(0.5)
    net.send_data('ROUTER1', [137,0,0,0,1])


def clean():
    net.send_data('ROUTER1', [131])
    time.sleep(0.5)
    net.send_data('ROUTER1', [135])


def get_data():
    net.send_data('ROUTER1', [142, 100])
