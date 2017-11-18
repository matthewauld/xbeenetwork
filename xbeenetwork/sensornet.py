import xbee
import logging
import serial
import time
from datetime import datetime
from nodes import *
import yaml
import os
import queue


class SensorNet(object):
    """The main xbee network, connected to xbee coordinator."""
    def __init__(self, port):
        """Start SensorNet."""
        self.packet_queue = queue.PriorityQueue()
        self._logger = logging.getLogger(__name__)
        self.serial = serial.Serial(port, baudrate=19200)
        self.config = yaml.safe_load(open(os.path.dirname(
            os.path.realpath(__file__)) + '/' + 'config.yml'))
        self.XB = xbee.ZigBee(self.serial,
                              shorthand=True,
                              callback=self.process_packet, escaped=True)
        self.units = {}
        self.XB.send('at', command='ND'.encode('ascii'))
        time.sleep(3)


    def process_packet(self, data):
        """Sort packet to proper processing function."""
        self._logger.debug("Incoming Packet {}".format(data))
        if data['id'] == 'at_response':
            self.process_at_response(data)
        elif self.units == {}:
            pass                    # Add fucntion to process data with no node
        elif data['id'] == 'rx':
            self.process_rx(data)

    def process_at_response(self, data):
        """Function that processes AT repsponse data."""
        if data['command'] == b'ND':
            self._update_node(data)

    def _update_node(self, data):
        """Create a node if none exists, or update node."""
        node_name = data['parameter']['node_identifier'].decode('ascii')
        try:
            node = self.units[node_name]
            if node.active:
                pass         # Add method to verify data in node, call here
            else:
                node.active = True
                node.active_time = datetime.node()
                self._logger.debug('Node "{0}" reactivated '.format(node_name,))

        except KeyError:

            if node_name in self.config['nodes'].keys():

                node_type = self.config['nodes'][node_name]
                if node_type == 'Roomba':
                    node = RoombaNode(data, self)
                    self.units[node_name] = node
                    self._logger.info('Node "{0}" registered as "{1}"'.format(node_name, node_type))
                else:
                    self._logger.error('Unrecognized node type "{0}" listed in config for {1}'.format(node_type, node_name))
            else:
                self.units[node_name] = BaseNode(data, self)
                self._logger.info('Node "{0}" registered as "BaseNode"'.format(node_name))

    def process_rx(self, data):
        """Add data to the main queue for processing."""
        node = None
        addr = data['source_addr']
        for key, item in self.units.items():
            if item.source_addr == addr:
                node = item
                node_name = key
                break
        if node is None:
            self._logger.warning("Packet from unknown source {}".format(data))
        else:
            node.process(data['rf_data'])


class Job(object):
    """Processing packet job to add to queue."""

    def __init__(self, node, data):
        self.node = node
        self.data = data
        self.priority = node.priority

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
