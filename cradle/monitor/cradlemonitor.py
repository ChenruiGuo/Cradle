# cradlemonitor.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

# Initialize Flask app and Socket.IO
app = Flask(__name__)
socketio = SocketIO(app)

# Store logs in memory
logs = []

@app.route('/')
def index():
    return render_template('index.html', logs=logs)

@socketio.on('connect')
def handle_connect():
    # Send all existing logs to the new client
    for log in logs:
        socketio.emit('log_update', log)

def send_log(message):
    """Function to send logs to the web UI."""
    logs.append(message)
    socketio.emit('log_update', message)

def start_web_ui():
    """Function to start the Flask + Socket.IO server."""
    print("Starting web UI...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)  # Bind to all available interfaces

if __name__ == '__main__':
    # For testing the web UI independently
    start_web_ui()