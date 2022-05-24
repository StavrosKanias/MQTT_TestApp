# API Server and MQTT publisher

import uvicorn
from fastapi import FastAPI, UploadFile, File
import random
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate subscriber ID with pub prefix randomly
subscriber_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'


def connect_mqtt():
    def on_connect(subscriber, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    subscriber = mqtt_client.Client(subscriber_id)
    subscriber.username_pw_set(username, password)
    subscriber.on_connect = on_connect
    subscriber.connect(broker, port)
    return subscriber


def publish(subscriber, msg):
    msg_count = 0
    #msg = f"messages: {msg_count}"
    result = subscriber.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1


def run():
    subscriber = connect_mqtt()
    subscriber.loop_start()
    app = FastAPI()

    @ app.post("/receive")
    async def receive(file: UploadFile = File(...)):
        contents = await file.read()
        publish(subscriber, contents)
    return app


if __name__ == '__main__':
    app = run()
    uvicorn.run(app, host='0.0.0.0', port=8000)
