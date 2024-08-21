from flask import request
from app import app

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    temperature = data.get('temperature')
    heartbeat = data.get('heartbeat')
    print(f"Temperature: {temperature} C, Heartbeat: {heartbeat} BPM")
    return "Data received", 200
