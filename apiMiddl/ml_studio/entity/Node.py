from .NodeProperty import NodeProperty
import json


class Node:

    def __init__(self, node_type, name, number_of_ports, properties: NodeProperty):
        self.node_type = node_type
        self.name = name
        self.number_of_ports = number_of_ports
        self.properties = properties

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
