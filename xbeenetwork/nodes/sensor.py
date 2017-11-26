from .basenode import BaseNode


class StandardSensor(BaseNode):
        def __init__(self, response, sensornet):
            """Initialize node with node discovery dict."""
            BaseNode.__init__(self, response, sensornet)
