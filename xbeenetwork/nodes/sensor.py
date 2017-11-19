from .basenode import BaseNode


class StandardSensor(BaseNode):
        def __init__(self, response, sensornet, config):
            """Initialize node with node discovery dict."""
            BaseNode.__init__(self, response, sensornet)
            self.pins = {}


        def set_mode(pin,state):
            command = 'D' + str(pin)
            self.send_command(command,state)
            self.pins[pin] = state
        
