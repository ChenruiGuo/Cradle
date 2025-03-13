from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import base64

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

# Generic Cradle String Message Updates
def send_generic_update(id_,message):
    """Send generic cradle update to the web UI."""
    match id_:
        case 'task_description':
            socketio.emit("task_update", message)
        case 'subtask_description':
            socketio.emit("subtask_update", message)
        case 'game_status':
            # this refers to the datetime + energy + weather + dialog + other
            socketio.emit("game_status_update", message)
        case 'action':
            socketio.emit("action_update", f"Last Action: {message}")
        case 'summarization':
            socketio.emit("summary_update", message)

    
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
    error_message = "Skill Action Executed Successfully" if not exec_info["errors"] else f"Execution Error Occurred: {exec_info['errors_info']}"
    socketio.emit("execution_info_update", error_message)

# Toolbar List
def send_toolbar(toolbar_info):
    """Send toolbar_info with toolbar (list) and selected_position (int) to the web UI"""
    socketio.emit("toolbar_update", toolbar_info)

# Image
def send_image(addr):
    """Process augmented screenshot image and send to the web UI"""
    try:
        with open(addr.replace("\\", "/"), "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            socketio.emit("screenshot_update", {"image": f"data:image/png;base64,{base64_image}"})
    except Exception as e:
        print(f"Error reading screenshot: {e}")

def start_web_ui():
    """Function to start the Flask + Socket.IO server."""
    print("Starting web UI...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)  # Bind to all available interfaces

if __name__ == '__main__':
    # For testing the web UI independently
    start_web_ui()