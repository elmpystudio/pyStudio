import json


class NodeProperty:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)