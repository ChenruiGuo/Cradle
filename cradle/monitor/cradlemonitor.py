from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

# Initialize Flask app and Socket.IO
app = Flask(__name__)
socketio = SocketIO(app)

# Store logs in memory
logs = []
cradle_status = "Ready"

@app.route('/')
def index():
    return render_template('index.html', logs=logs, status=cradle_status)

#@socketio.on('connect')
#def handle_connect():
    # Send all existing logs to the new client
#    for log in logs:
#        socketio.emit('log_update', log)

def add_log(log_data):
    """Add a log to the logs array and send it to all connected clients."""
    logs.append(log_data)
    socketio.emit('log_update', log_data)

@socketio.on("control")
def handle_control(action):
    """Handle Play, Pause, and Stop actions from the frontend."""
    global cradle_status
    if action == "play":
        cradle_status = "Running"
    elif action == "pause":
        cradle_status = "Paused"
    elif action == "stop":
        cradle_status = "Stopped"

    # Broadcast the updated status to all clients
    socketio.emit("status_update", cradle_status)

def get_status():
    global cradle_status
    return cradle_status

def start_web_ui():
    """Function to start the Flask + Socket.IO server."""
    print("Starting web UI...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)  # Bind to all available interfaces

if __name__ == '__main__':
    # For testing the web UI independently
    start_web_ui()