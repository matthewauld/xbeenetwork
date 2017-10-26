"""
The base xbee sensor node.

All other node types must be a modificationof this.
"""
from queue import Queue


class BaseNode(object):
    """Base Node class."""

    def __init__(self, sensornet, response):
        """Initialize node with node discovery dict."""
        self.source_addr = response['parameter']['source_addr']
        self.source_addr_long = response['parameter']['source_addr_long']
        self.parent_address = response['parameter']['parent_address']
        self.profile_id = response['parameter']['profile_id']
        self.manufacturer = response['parameter']['manufacturer']
        self.node_identifier = response['parameter']['node_identifier']
        self.device_type = response['parameter']['device_type']
        self.active = True
        self.data = Queue(1024)
        self.sensornet = sensornet
