from csv import DictWriter
import string
import paho.mqtt.client as mqtt
import json


client = mqtt.Client()
client.connect('0.0.0.0', 1883)


def on_connect(client, userdata, flags, rc):
    print("Connected to a broker")
    client.subscribe("sig/a")


def on_message(client, userdata, msg):
    test = msg.payload.decode("utf-8")
   
    with open('data.json', 'w') as f:
        test = json.loads(test)
        json.dump(test, f, indent=4)


while True:
    client.loop_start()
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_stop()


