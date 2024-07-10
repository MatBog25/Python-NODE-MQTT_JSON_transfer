import paho.mqtt.client as mqtt
import json


client = mqtt.Client()
client.connect('0.0.0.0', 1883)


with open("data2.json", encoding='utf-8') as file:
    test = json.load(file)
    data = json.dumps(test, indent = 4)


client.publish("sig/a", str(data))


