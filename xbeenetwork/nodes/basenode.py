"""
The base xbee sensor node.

All other node types must be a modification of this.
"""
from datetime import datetime
import struct
import logging


class BaseNode(object):
    """Base Node class."""

    def __init__(self, response, sensornet):
        """Initialize node with node discovery dict."""
        self.source_addr = response['source_addr']
        self._logger = logging.getLogger(__name__)

        self.source_addr_long = response['source_addr_long']
        self.parent_address = response['parent_address']
        self.manufacturer = response['manufacturer']
        self.node_identifier = response['node_identifier']
        self.active = True
        self.active_time = datetime.now()
        self.sensornet = sensornet
        self.pins = {'dio-0':{},'dio-1':{},'dio-2':{},'dio-3':{},'dio-4':{},
            'dio-5':{},'dio-6':{},'dio-7':{},'dio-8':{},'dio-9':{},'dio-10':{},'dio-11':{}}


    def send_data(self, data):
        """Simple send data request."""
        self.sensornet.XB.send('tx', dest_addr=self.source_addr,
                               dest_addr_long=self.source_addr_long, data=data)
    def send_command(self,command_type, parameter_data=None):
        '''Send at command'''
        if parameter_data != None:

            self.sensornet.XB.send('remote_at',dest_addr=self.source_addr,
                                   dest_addr_long=self.source_addr_long,
                                   command=command_type,parameter=parameter_data)
        else:
           self.sensornet.XB.send('remote_at',dest_addr=self.source_addr,
                                  dest_addr_long=self.source_addr_long,
                                  command=command_type)

    def set_pin_mode(self,pin,state):
        """Sets the current mode of a pin."""
        command = 'D' + str(pin)
        data = struct.pack('>B',state)
        self.send_command(command,data)
        self.pins['dio-'+str(pin)]['state'] = state

    def set_sample_rate(self, milliseconds):
        """Set the frequency that pins with a set input state return data."""
        data = struct.pack('>B',milliseconds)
        self.send_command('IR',data)
        self.sample_rate = miliseconds

    def set_detector_pins(self,pins):
        """Set digital input pins which trigger a polling on change."""
        data = 0
        for pin in pins:
            data += 2**pin
            self.pins['dio-'+str(pin)]['detector'] = True
        data = struct.pack('>H',data)
        self.send_command('IC',data)

    def set_sleep_mode(mode,milliseconds):
        """ Sets if any how the node will sleep."""
        self.send_command('SM',mode)
        data = struct.pack('>B',int(milliseconds/10))
        self.send_command('SP',data)
        self.sleep_mode = mode

    def process_io(self,data):
        """Processes incoming pin states into self.pins unless overridden"""
        print('AAAAAAAAA')
        for pin, reading in data[0].items():
            self._logger.debug('Updated pin: {}:{}'.format(pin,data))
            self.pins[pin]['data'] = reading





ADC_PIN = 2
DIGITAL_INPUT = 3
DIGITAL_LOW = 4
DIGITAL_HIGH = 5
NO_SLEEP = 0
PIN_HIBERNATE = 1
CYCLIC_SLEEP = 4
CYCLIC_SLEEP_PIN_WAKE = 5
