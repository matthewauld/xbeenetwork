import xbee
import logging
import sys
import serial
import time
import nodes


class SensorNet(object):
    def __init__(self, port):
        self._logger = logging.getLogger(__name__)
        self.serial = serial.Serial(port)
        self.XB = xbee.ZigBee(self.serial, shorthand=True, callback=self.process_packet, escaped=True)
        self.units = {}
        self.XB.send('at', command='ND'.encode('ascii'))
        time.sleep(3)

    # guide for processing all packets
    def process_packet(self, data):
        self._logger.debug("Incoming Packet {}".format(data))
        if data['id'] == 'at_response':
            self.process_at_response(data)
        elif self.units == {}:
            pass
        elif data['id'] == 'rx':
            self.process_rx(data)

    def process_at_response(self, data):
        ''' Function that processes AT repsponse data '''

        if data['command'] == b'ND':
            self.units[data['parameter']
                       ['node_identifier']] = data['parameter']

    def process_rx(self, data):
        """Function that processes RF response data."""
        for byte in data['rf_data']:
            self._logger.debug("Byte: {}".format(byte))

    def send_data(self, unit, data):
        """Simple send data request.

        First byte is always length of rest of data.
        Must be in bytes format.
        """
        try:
            unit = unit.encode('ascii')
        except AttributeError:
            pass
        data = [len(data)]+data
        self.XB.send('tx', dest_addr=self.units[unit]['source_addr'], dest_addr_long=self.units[unit]['source_addr_long'], data=bytes(data))