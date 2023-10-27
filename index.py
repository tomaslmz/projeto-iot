from flask import Flask, render_template, request, jsonify
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
    try:
        data = json.loads(msg.payload)
        socketio.emit('data', data)
        if(data['temp'] > 26):
            subscribe.publish('status', 'A janela está aberta!')
        else:
            subscribe.publish('status', 'A janela está fechada!')
    except json.JSONDecodeError:
        print(f"Payload was not a valid JSON: {msg.payload}")

subscribe = mqtt.Client()
# subscribe.username_pw_set(user, password)
subscribe.connect(address, port)
subscribe.subscribe(topic)
subscribe.on_message = on_message

@socketio.on('connect')
def handle_connect():
    print(data) 
    socketio.emit('data', data)

@app.route("/window/state", methods = ['POST'])
def handle_request():
    state = request.json['state']

    data = json.dumps({'state': state})

    subscribe.publish('flask', data)
    return 'ok'

@app.route("/")
def index():
    return render_template('index.html')

# if __name__ == '__main__':
subscribe.loop_start()
socketio.run(app, host='0.0.0.0', port=5000)