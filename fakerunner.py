import time
import threading
from cradle.log import Logger
from cradle.monitor import start_web_ui, get_status, send_stage_update

logger = Logger()
STAGES = ["1 Information Gathering", "2 Self Reflection", "3 Task Inference", "4 Skill Curation", "5 Action Planning"]


def check_status():
    """Check the current status and handle pause/stop behavior."""
    if get_status()=="Stopped":
        print("Stopping program...")
        return False # Add command here to terminate program
    elif get_status()=="Paused":
        print("Program paused... Waiting to resume.")
        while get_status()=="Paused":  # If paused, keep checking status every 2s
            time.sleep(2)
    return get_status()=="Running"

def run_program():
    """Your existing program logic."""
    print("Press the play button to start Cradle!")
    while get_status()=="Ready":
        time.sleep(2)
    count = 0
    while True:
        count += 1
        send_stage_update(0)
        write_message = f"Fakerunner log {count}"
        logger.write(write_message)  # Call to logger
        time.sleep(5)
        send_stage_update(1)
        time.sleep(2)
        send_stage_update(2)

        if not check_status():
            break

        warn_message = f"This is a fucking warning {count}"
        logger.warn(warn_message)  # Call to logger
        time.sleep(3)  # Simulate some work
        send_stage_update(3)
        time.sleep(3)  # Simulate some work
        send_stage_update(4)
        time.sleep(3)  # Simulate some work

        if not check_status():
            break

if __name__ == '__main__':
    # Start the web UI in a separate thread
    web_ui_thread = threading.Thread(target=start_web_ui, daemon=True)
    web_ui_thread.start()

    # Run your existing program
    run_program()