import xbee
import logging
import serial
import time
from datetime import datetime
from nodes import *
import yaml
import os



class SensorNet(object):
    """The main xbee network, connected to xbee coordinator."""
    def __init__(self, port):
        """Start SensorNet."""
        self._logger = logging.getLogger(__name__)
        self.serial = serial.Serial(port, baudrate=19200)
        self.config = yaml.safe_load(open(os.path.dirname(
            os.path.realpath(__file__)) + '/' + 'config.yml'))
        self.XB = xbee.ZigBee(self.serial,
                              shorthand=True,
                              callback=self.process_packet, error_callback=self.error_callback escaped=True)
        self.units = {}
        self.XB.send('at', command='ND'.encode('ascii'))
        time.sleep(3)

    def error_callback(self, err):
        self._logger.warning(err)

    def process_packet(self, data):
        """Sort packet to proper processing function."""
        self._logger.debug("Incoming Packet {}".format(data))
        if data['id'] == 'at_response':
            self.process_at_response(data)
        elif data['id'] == 'rx':
            self.process_rx(data)
        elif data['id'] == 'rx_io_data_long_addr':
            self.process_io(data)
        elif data['id'] == 'node_id_indicator':
            self.process_node_id_response(data)
        elif self.units == {}:
            pass                    # Add fucntion to process data with no node
        else:
            self._logger.debug("Incoming Packet {}".format(data))

    def process_at_response(self, data):
        """Function that processes AT repsponse data."""
        if data['command'] == b'ND':
            response = {'source_addr':data['parameter']['source_addr'],'source_addr_long':data['parameter']['source_addr_long'],'parent_address':data['parameter']['parent_address'],'manufacturer':data['parameter']['manufacturer'],'node_identifier':data['parameter']['node_identifier']}
            self._update_node(response)
        else:
            self._logger.debug("Unknown AT Response {}".format(data))

    def process_node_id_response(self, data):
        """Processes data from notes when they join the PAN."""
        response = {'source_addr':data['source_addr'],'source_addr_long':data['source_addr_long'],'parent_address':data['parent_source_addr'],'manufacturer':data['manufacturer_id'],'node_identifier':data['node_id']}
        self._update_node(response)

    def _update_node(self, data):
        """Create a node if none exists, or update node."""
        node_name = data['node_identifier'].decode('ascii')
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

                node_type = self.config['nodes'][node_name]['type']
                if node_type == 'Roomba':
                    node = RoombaNode(data, self)
                    self.units[node_name] = node
                    self._logger.info('Node "{0}" registered as "{1}"'.format(node_name, node_type))
                elif node_type == 'StandardSensor':
                    node = StandardSensor(data, self)
                    self.units[node_name] = node
                    self._logger.info('Node "{0}" registered as "{1}"'.format(node_name, node_type))
                else:
                    self._logger.error('Unrecognized node type "{0}" listed in config for {1}'.format(node_type, node_name))
            else:
                self.units[node_name] = BaseNode(data, self)
                self._logger.info('Node "{0}" registered as "BaseNode"'.format(node_name))

    def process_rx(self, data):
        """Process incoming RX data using node specific function."""
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
            node.process_rx(data['rf_data'])

    def process_io(self,data):
        """Process incoming IO data using node specific functon."""
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
            node.process_io(data['samples'])

    def halt(self):
        """Closes serial ports and exits."""
        self.XB.halt()
        self.serial.close()
        return True

    def __del__(self):
        self.halt()
