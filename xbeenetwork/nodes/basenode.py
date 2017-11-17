"""
The base xbee sensor node.

All other node types must be a modificationof this.
"""
from datetime import datetime
from queue import Queue


class BaseNode(object):
    """Base Node class."""

    def __init__(self, response, sensornet):
        """Initialize node with node discovery dict."""
        self.priority = 10
        self.source_addr = response['parameter']['source_addr']
        self.source_addr_long = response['parameter']['source_addr_long']
        self.parent_address = response['parameter']['parent_address']
        self.profile_id = response['parameter']['profile_id']
        self.manufacturer = response['parameter']['manufacturer']
        self.node_identifier = response['parameter']['node_identifier']
        self.device_type = response['parameter']['device_type']
        self.active = True
        self.active_time = datetime.now()
        self.sensornet = sensornet

    def send_data(self, data):
        """Simple send data request."""
        self.sensornet.XB.send('tx', dest_addr=self.source_addr,
                               dest_addr_long=self.source_addr_long, data=data)
    def process_data(self, data):
        
