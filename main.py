import paho.mqtt.client as mqtt
import random
import json
import requests
import bs4
import time

import model.ControlMessage
import thread

host = "19november.freeddns.org"
port = 5384
control_topic = "music-downloader/control"
health_topic = "music-downloader/agent/health"


def on_connect(_client, userdata, flags, rc):
    print "Connected with result code " + str(rc)
    print "Subscribing to topic " + control_topic
    _client.subscribe(control_topic, qos=1)
    print "Initializing completed"


def on_message(_client, userdata, msg):
    print "Message arrived from " + msg.topic
    print str(msg.payload)
    control_message = model.ControlMessage.from_string(str(msg.payload))
    handle_message(_client, control_message)


def handle_message(_client, control_message):
    data = requests.get(control_message.url).content
    soup = bs4.BeautifulSoup(data, "html.parser")
    player_element = soup.select("div#html5player")
    if len(player_element) > 0:
        data_source = player_element.pop().attrs['data-xml']
    else:
        print "Cannot get data_source URL"
        _client.publish(control_message.responseTopic, "{}", qos=1)
        return

    # Load playlist json data
    playlist_data = json.loads(requests.get(data_source).content)
    playlist_items = playlist_data['data']
    items = []
    for item_json in playlist_items:
        source = ""
        if len(item_json['source_list']) > 0:
            source = item_json['source_list'][0]
        item = {
            "Title": item_json['name'],
            "Performer": item_json['artist'],
            "Source": source,
            "Duration": "",
            "HQ": "",
            "Link": "",
            "ErrorMessage": "",
            "ErrorCode": "",
            "F360": "",
            "F480": "",
            "F720": "",
            "F1080": "",
        }
        items.append(item)

    response = {
        "ItemList": items
    }

    response_string = json.dumps(response)

    print response_string
    print "Publishing to topic " + control_message.responseTopic
    _client.publish(control_message.responseTopic, response_string, qos=1)


def on_disconnect(_client, userdata, rc):
    print "Disconnected to broker"


def health_monitor(_client):
    while True:
        try:
            _client.publish(health_topic, "Agent is online", qos=1)
        except:
            print "Failed to publish health message"

        time.sleep(30)


if __name__ == "__main__":
    print "Starting daemon..."

    client = mqtt.Client(client_id="mqtt-client-" + str(random.random()))
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(host=host, port=port)

    thread.start_new_thread(health_monitor, (client,))

    client.loop_forever()
