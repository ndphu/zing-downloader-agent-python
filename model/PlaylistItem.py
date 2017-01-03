import json


def from_string(json_string):
    data_json = json.loads(json_string)
    return PlaylistItem(data_json)


class PlaylistItem:
    title = ""
    performer = ""
    source = ""
    duration = ""
    HQ = ""
    link = ""
    errorMessage = ""
    errorCode = ""
    F360 = ""
    F480 = ""
    F720 = ""
    F1080 = ""

    def __init__(self, data_json):
        self.id = data_json['id']
        self.name = data_json['name']
        self.artist = data_json['artist']
        self.link = data_json['link']
        self.cover = data_json['cover']
        self.qualities = data_json['qualities']
        self.source_list = data_json['source_list']
        self.source_base = data_json['source_base']
