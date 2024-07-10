const mqtt = require('mqtt')
const fs = require('fs')

var config = {
    "Broker1": "mqtt://test.mosquitto.org",
    "Broker1_port": 1883,
}


var client = mqtt.connect(config.Broker1, {port: config.Broker1_port})


client.on('connect', () => {
    client.subscribe('sig/a', (err) => {
        if(err) {
            console.error(`Error subscribe to sig/a: ${err}`)
        } else {
            // fs.writeFile('data.json', )
        }
    })
})

client.on('message', (topic, payload) => {
    console.log(`${topic}: ${payload.toString()}`)
    fs.writeFileSync('data.json', payload.toString())
})

