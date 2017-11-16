"""Node attached to Roomba."""

import logging
import struct
from .basenode import BaseNode
from  .opcodes import sensorpackets
import math


class RoombaNode(BaseNode):
    """Roomba Node class."""

    def __init__(self, response, sensornet):
        """Initialize node with node discovery dict."""
        BaseNode.__init__(self, response, sensornet)
        self.mode = MODE_OFF
        self.priority = 2
        self.sensors = {}
        self._logger = logging.getLogger(__name__)
        self.distance = 0                   #distance travelled since initiated
        self.angle = 0                     #radius turned since initiated
        self.location = [(0,0)]
        self.flag = False

    def send_data(self, senddata):
        """Simple send data request.

        First byte is always length of rest of data.
        Must be in bytes format.
        """
        self.flag =True
        senddata = bytes([len(senddata)]) + senddata             #append len byte
        print(senddata)
        self.sensornet.XB.send('tx', dest_addr=self.source_addr,
                               dest_addr_long=self.source_addr_long,
                               data=senddata)

        """################
        DATA PROCESSING
        ################"""

    def process(self, data):
        #self._logger.debug("Incoming Packet {}".format(data))
        """Update the sensor status from any packets that appear."""
        '''if self.validate_checksum(data) is False:
            self._logger.error("Invalid checksum for packet {}".format(str(data)))
            return False'''
        opcode = struct.unpack_from('B', data)[0]       # Not used currently
        packet_length = struct.unpack_from('B', data, offset=1)[0]

        i = 2          # Set i = 1 to skip opcode and length
        while i <= packet_length:    # Exclude checksum
            #unpack sensor code
            sensor_code = struct.unpack_from('B', data, offset=i)[0]
            i += 1
            #get datatype
            packet_type = sensorpackets[sensor_code]
            #unpack data
            sensor_data = struct.unpack_from(packet_type[1], data, offset=i)[0]
            i += struct.calcsize(packet_type[1])
            #process specific datat types
            if sensor_code == 19:
                self.distance += sensor_data
            elif sensor_code == 20:
                self.angle += sensor_data
            else:
                #if nothing specific to do with data, add it to the general senor dict
                self.sensors[packet_type[0]] = sensor_data

    def validate_checksum(self, data):
        """Ensure incoming packet is valid."""
        y = 0
        for i in range(1, len(data)):   # start at 1 to skip opcode
            y += data[i]
        y = y & 0xFF
        if y == 0:
            return True
        else:
            return False

    def start(self):
        """Set to Passive Mode."""
        self.set_mode(MODE_PASSIVE)

    """################
    API CONTROL
    ################"""

    def set_mode(self, mode):
        """Change the roomba's mode.

        Options: MODE_PASSIVE, MODE_OFF, MODE_SAFE, MODE_FULL
        """
        self.mode = mode

        self.send_data(bytes([mode]))

    def automation(self, action):
        """Start an automation.

        Options: CLEAN, MAX, SPOT, DOCK
        """
        self.send_data(bytes([action]))

    def drive(self, velocity, radius, mode=131):    #set to cetain
        if mode in [133, 138]:
            self.set_mode(mode)
        data = bytes([137]) + struct.pack('>h', velocity) + struct.pack('>h', radius)
        self.send_data(data)

    def move(self, velocity, distance):  # NOTE: add fucntion to ensure stream is on!
        start_distance = self.distance
        self.drive(velocity, 0)
        while (start_distance + distance >= self.distance):
            print(self.distance - start_distance)
        self.drive(0,0)
        #self._plot_location(self.distance-start_distance)
        return True


    def turn(self, velocity, radius): # NOTE: add fucntion to ensure stream is on!
        start_angle = self.angle
        if radius >= 0:
            turn = 1
        else:
            turn = 0
        self.drive(velocity, turn)
        while (start_angle + radius < self.angle) or (start_angle - radius > self.angle):
            pass
        self.drive(0,0)
        return True

    def _plot_location(self, distance):
        radius = self.angle % 360
        if radius < 0:
            radius += 360
        x_distance = math.sin(radius)*distance
        y_distance = math.sqrt(x_distance**2+distance**2)
        last_point = self.location[-1]
        current_point = (last_point[0]+x_distance,last_point[1]+y_distance)
        self.location.append(current_point)

    def start_stream(self):
        self.send_data(bytes([148, 3, 19, 20, 21]))

    def pause_stream(self):
        self.send_data(bytes([150, 0]))





MODE_OFF = 133          # Currently no way to turn on except at startup.
MODE_PASSIVE = 128
MODE_SAFE = 131
MODE_FULL = 132

CLEAN = 135
MAX = 136
SPOT = 134
DOCK = 143
