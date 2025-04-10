import json
import time

from flask import Flask,Response, jsonify
from flask_cors import CORS
from .sensor import SensorData

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) #svelte dev server
sensor=SensorData()

@app.route('/')
def root():
    return jsonify({"message":"Welcome to the Sensor Dashboard API"})

@app.route("/current")
def get_current_reading():
    # Get current sensor reading
    return jsonify(sensor.generate_reading())

@app.route("/stream")
def stream_data():
    # strem sensor data using server side events
    def generate():
        while True:
            data = sensor.generate_reading()
            yield f"event: sensor_update\ndata: {json.dumps(data)}\n\n"
            time.sleep(2)  #update every 2 seconds
    
    return Response(generate(),mimetype="text/event-stream")
