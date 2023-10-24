from flask import Flask, render_template
import paho.mqtt.client as mqtt
import json
import mysql.connector
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

address = 'mqtt.eclipseprojects.io' 
port = 1883
topic = 'wokwi'

data = ''

def on_message(client, userdata, msg):
    # print('oi')
    data = json.loads(msg.payload)
    # print(json.loads(msg.payload))
    socketio.emit('data', data)

subscribe = mqtt.Client()
# subscribe.username_pw_set(user, password)
subscribe.connect(address, port)
subscribe.subscribe(topic)
subscribe.on_message = on_message

@socketio.on('connect')
def handle_connect():
    print(data)
    socketio.emit('data', data)

@app.route("/")
def index():
    return render_template('index.html')

# if __name__ == '__main__':
subscribe.loop_start()
socketio.run(app, host='0.0.0.0', port=5000)