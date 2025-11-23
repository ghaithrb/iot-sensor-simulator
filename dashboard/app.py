from __future__ import annotations
import threading
import json
from collections import deque
from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt

BROKER_HOST = 'localhost'
BROKER_PORT = 1883
TOPICS = ['iot/sensor/temperature', 'iot/sensor/humidity', 'iot/sensor/gps']

app = Flask(__name__)
latest = {t: None for t in TOPICS}
history = {t: deque(maxlen=200) for t in TOPICS}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        for t in TOPICS:
            client.subscribe(t)
    else:
        print('MQTT connect failed', rc)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
    except Exception:
        payload = {'raw': msg.payload.decode('utf-8', 'ignore')}
    latest[msg.topic] = payload
    history[msg.topic].append({'timestamp': payload.get('timestamp'), 'payload': payload})


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def start_mqtt():
    mqtt_client.connect(BROKER_HOST, BROKER_PORT, 60)
    mqtt_client.loop_start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/latest')
def api_latest():
    return jsonify(latest)


@app.route('/api/history')
def api_history():
    return jsonify({k: list(v) for k, v in history.items()})


if __name__ == '__main__':
    start_mqtt()
    app.run(host='0.0.0.0', port=5000, debug=True)
