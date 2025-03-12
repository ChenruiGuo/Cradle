from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

# Initialize Flask app and Socket.IO and cradlemonitor
app = Flask(__name__)
socketio = SocketIO(app)
#logs = []
cradle_status = "Ready"
STAGES = ["1 Information Gathering", "2 Self Reflection", "3 Task Inference", "4 Skill Curation", "5 Action Planning"]


@app.route('/')
def index():
    return render_template('index.html', status=cradle_status)

# For refreshes to the web ui
#@socketio.on('connect')
#def handle_connect():
#    # Send all existing logs to the new client
#    for log in logs:
#        socketio.emit('log_update', log)

# Logs
def add_log(log_data):
    """Add a log to the logs array and send it to all connected clients."""
    #logs.append(log_data)
    socketio.emit('log_update', log_data)

# Control Buttons
@socketio.on("control")
def handle_control(action):
    """Handle Play, Pause, and Stop actions from the frontend."""
    global cradle_status
    if action == "play":
        cradle_status = "Running"
    elif action == "pause" and cradle_status == "Running":
        cradle_status = "Pausing"
    elif action == "stop":
        cradle_status = "Stopping"

    # Broadcast the updated status to all clients
    socketio.emit("status_update", cradle_status)

# Cradle Status
def get_status():
    global cradle_status
    return cradle_status

def set_status(new_status):
    global cradle_status
    cradle_status = new_status
    socketio.emit("status_update", cradle_status)

# Cradle Stage Pills
def send_stage_update(iter,stage_index):
    """Emit the current stage index to all connected clients."""
    send_chat_message("Cradle", f"=== Iteration {iter}: {STAGES[stage_index]} ===")
    socketio.emit("stage_update", stage_index)

# GPT-4O Live Chat Messages
def send_chat_message(sender, message):
    """Send a chat message to the web UI."""
    socketio.emit("chat_message", {"sender": sender, "message": message})

# Generic Cradle Updates
def send_generic_update(id_,message):
    """Send generic cradle update to the web UI."""
    match id_:
        case 'task_description':
            socketio.emit("task_update", message)
        case 'subtask_description':
            socketio.emit("subtask_update", message)
        case 'game_status':
            socketio.emit("game_status_update", message)
    
# Skill Library Updates
def send_skill_library(skills):
    """Process and send skill library array to the web UI"""  
    processed_skills = [
        {"name": skill["function_expression"], "description": skill["description"]}
        for skill in skills
    ]
    socketio.emit("skill_update", processed_skills)

# Execution Info
def send_exec_info(exec_info):
    """Process exec info object and send to the web UI"""

    socketio.emit()

# Toolbar List
def send_toolbar(toolbar_dict_list, id_):
    """Process toolbar dict list and selected position and send to the web UI"""

    socketio.emit()

# Image
def send_image(image):
    """Process augmented screenshot image and send to the web UI"""

    socketio.emit("screenshot_update",)

def start_web_ui():
    """Function to start the Flask + Socket.IO server."""
    print("Starting web UI...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)  # Bind to all available interfaces

if __name__ == '__main__':
    # For testing the web UI independently
    start_web_ui()