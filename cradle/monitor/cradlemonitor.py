from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

# Initialize Flask app and Socket.IO
app = Flask(__name__)
socketio = SocketIO(app)

# Store logs in memory
logs = []
cradle_status = "Ready"
STAGES = ["1 Information Gathering", "2 Self Reflection", "3 Task Inference", "4 Skill Curation", "5 Action Planning"]


@app.route('/')
def index():
    return render_template('index.html', logs=logs, status=cradle_status)

# For refreshes to the web ui
@socketio.on('connect')
def handle_connect():
    # Send all existing logs to the new client
    for log in logs:
        socketio.emit('log_update', log)

# Memory Logs
def add_log(log_data):
    """Add a log to the logs array and send it to all connected clients."""
    logs.append(log_data)
    socketio.emit('log_update', log_data)

# Control Buttons
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

# Cradle Status
def get_status():
    global cradle_status
    return cradle_status

# Cradle Stage Pills
def send_stage_update(iter,stage_index):
    """Emit the current stage index to all connected clients."""
    send_chat_message("Cradle", f"=== Iteration {iter}: {STAGES[stage_index]} ===")
    socketio.emit("stage_update", stage_index)

# GPT-4O Live Chat Messages
def send_chat_message(sender, message):
    """Send a chat message to the web UI."""
    socketio.emit("chat_message", {"sender": sender, "message": message})

def start_web_ui():
    """Function to start the Flask + Socket.IO server."""
    print("Starting web UI...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)  # Bind to all available interfaces

if __name__ == '__main__':
    # For testing the web UI independently
    start_web_ui()