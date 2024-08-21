from threading import Thread
from app import app
import json, blockchain,time,requests, serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from cryptography.fernet import Fernet
import base64

# Firebase configuration
cred = credentials.Certificate('cred/mobile-app-mfa-firebase.json')  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mobile-app-mfa.firebaseio.com/' 
})  # Add the database URL here
db = firestore.client()

# Read the key from the file
with open('encryption_key.txt', 'rb') as key_file:
    key = key_file.read()
f = Fernet(key)

# Function to handle the serial communication and sending data to Flask app and Firebase
def serial_to_flask_and_firebase():
    # Serial port configuration
    serial_port = 'COM10'  
    baud_rate = 9600
    ser = serial.Serial(serial_port, baud_rate)

    # Flask server URL
    flask_url = 'http://127.0.0.1:5000/receive_data'

    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                # Assuming the data is sent in the format: Temperature: XX.XX C, Heart Beat: YY BPM
                data_parts = line.split(',')
                temperature_str = data_parts[0].split(':')[1].strip().replace(' C', '')
                heartbeat_str = data_parts[1].split(':')[1].strip().replace(' BPM', '')

                temperature = float(temperature_str)
                heartbeat = int(heartbeat_str)

                data = {
                    'temperature': temperature,
                    'heartbeat': heartbeat
                }

                # Encrypt the data
                data_json = json.dumps(data)  # Convert data to JSON string
                encrypted_data = f.encrypt(data_json.encode())
                encrypted_data_str = base64.b64encode(encrypted_data).decode()  # Encode for storage

                # Send encrypted data to Flask
                response = requests.post(flask_url, json={'encrypted_data': encrypted_data_str})
                print(f"Encrypted data sent to Flask: {encrypted_data_str}, Response: {response.text}")

                # Alos encrypted data to Firebase with timestamp
                timestamp = time.time()
                doc_ref = db.collection('health_log').document()
                doc_ref.set({
                    'timestamp': timestamp,
                    'encrypted_data': encrypted_data_str
                })
                print(f"Encrypted data logged to Firebase: {encrypted_data_str}, Timestamp: {timestamp}")

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == '__main__':
    # Start the serial communication thread
    serial_thread = Thread(target=serial_to_flask_and_firebase)
    serial_thread.start()

    # Start the Flask app
    app.run(debug=True)
