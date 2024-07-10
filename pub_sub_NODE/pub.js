const mqtt = require('mqtt')
const fs = require('fs')


var config = {
    "Broker2": "mqtt://test.mosquitto.org",
    "Broker2_port": 1883,
}


var client2 = mqtt.connect(config.Broker2, {port: config.Broker2_port})

let jsonData = require('./data2.json');

console.log(jsonData);

client2.on('connect', function () {
    client2.publish('sig/a', JSON.stringify(jsonData))
})