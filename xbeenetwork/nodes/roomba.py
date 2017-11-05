"""Node attached to Roomba."""

from .basenode import BaseNode


class RoombaNode(BaseNode):
    """Roomba Node class."""

    def __init__(self, response, sensornet):
        """Initialize node with node discovery dict."""
        BaseNode.__init__(self, response, sensornet)
        self.mode = MODE_OFF
        self.priority = 2

    def send_data(self, data):
        """Simple send data request.

        First byte is always length of rest of data.
        Must be in bytes format.
        """
        data = [len(data)]+data
        self.sensornet.XB.send('tx', dest_addr=self.source_addr,
                               dest_addr_long=self.source_addr_long,
                               data=bytes(data))
    def process(self,data):

    def start(self):
        """Set to Passive Mode."""
        self.set_mode(MODE_PASSIVE)

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
