"""Node attached to Roomba."""

import logging
from .basenode import BaseNode
import struct
from  .opcodes import sensorpackets


class RoombaNode(BaseNode):
    """Roomba Node class."""

    def __init__(self, response, sensornet):
        """Initialize node with node discovery dict."""
        BaseNode.__init__(self, response, sensornet)
        self.mode = MODE_OFF
        self.priority = 2
        self.sensors = {}
        self._logger = logging.getLogger(__name__)

    def send_data(self, data):
        """Simple send data request.

        First byte is always length of rest of data.
        Must be in bytes format.
        """
        data = [len(data)]+data
        self.sensornet.XB.send('tx', dest_addr=self.source_addr,
                               dest_addr_long=self.source_addr_long,
                               data=bytes(data))

        """################
        DATA PROCESSING
        ################"""

    def process(self, job):
        """Update the sensor status from any packets that appear."""
        data = job.data
        if self.validate_checksum(data) is False:
            self._logger.error("Invalid checksum for packet {}".format(str(data)))
            return False
        #opcode = struct.unpack_from('B',data)[0]       # Not used currently
        packet_length = struct.unpack_from('B',data)[1]

        i = 2          # Set i = 1 to skip opcode and length
        while i < packet_length - 1:    # Exclude checksum
            sensor_code = struct.unpack_from('B', data, i)
            i += 1
            packet_type = sensorpackets[sensor_code]
            data = struct.unpack_from(packet_type[1], data, i)
            i += struct.calcsize(packet_type[1])
            self.sensors[packet_type[0]] = data

    def validate_checksum(data):
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

        self.send_data([mode])

    def automation(self, action):
        """Start an automation.

        Options: CLEAN, MAX, SPOT, DOCK
        """
        self.send_data([action])

    def move_forwards(self, mode=131):
        """Move roomba forwards."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.send_data([137, 0, 255, 0, 0])

    def rotate_left(self, mode=131):
        """Move roomba forwards."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.send_data([137, 0, 255, 0, 1])

    def rotate_right(self, mode=131):
        """Move roomba forwards."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.send_data([137, 0, 255, 255, 255])

    def stop(self, mode=131):
        """Stop roomba."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.send_data([137, 0, 0, 0, 0])

    def move_backwards(self, mode=131):
        """Move roomba backwards."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.send_data([137, 255, 1, 0, 0])


MODE_OFF = 133          # Currently no way to turn on except at startup.
MODE_PASSIVE = 128
MODE_SAFE = 131
MODE_FULL = 132

CLEAN = 135
MAX = 136
SPOT = 134
DOCK = 143
