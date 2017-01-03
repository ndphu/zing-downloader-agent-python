import json


def from_string(s):
    return json.loads(s, object_hook=lambda obj: ControlMessage(obj["url"], obj["responseTopic"]))


class ControlMessage(object):
    url = None
    responseTopic = None

    def __init__(self, url, response_topic):
        self.url = url
        self.responseTopic = response_topic
