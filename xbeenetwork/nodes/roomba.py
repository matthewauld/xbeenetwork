"""Node attached to Roomba."""

from .basenode import BaseNode


class RoombaNode(BaseNode):
    """Roomba Node class."""

    def __init__(self, sensornet, response):
        """Initialize node with node discovery dict."""
        BaseNode.__init__(sensornet, response)
        self.mode = MODE_OFF

    def start(self):
        """Set to Passive Mode."""
        self.set_mode(MODE_PASSIVE)

    def set_mode(self, mode):
        """Change the roomba's mode.

        Options: MODE_PASSIVE, MODE_OFF, MODE_SAFE, MODE_FULL
        """
        self.mode = mode

        self.sensornet.send_data([mode])

    def automation(self, action):
        """Start an automation.

        Options: CLEAN, MAX, SPOT, DOCK
        """
        self.sensornet.send_data([action])

    def move_forwards(self, mode=131):
        """Move roomba forwards."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.sensornet.send_data([137, 0, 50, 0, 0])

    def stop(self, mode=131):
        """Stop roomba."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.sensornet.send_data([137, 0, 0, 0, 0])

    def move_backwards(self, mode=131):
        """Move roomba backwards."""
        if mode in [133, 138]:
            self.set_mode(mode)
        self.sensornet.send_data([137, 255, 206, 0, 0])



MODE_OFF = 133          # Currently no way to turn on except at startup.
MODE_PASSIVE = 128
MODE_SAFE = 131
MODE_FULL = 132

CLEAN = 135
MAX = 136
SPOT = 134
DOCK = 143
