# fakerunner.py
import time
import threading
from cradlemonitor import send_log, start_web_ui

def run_program():
    """Your existing program logic."""
    count = 0
    while True:
        time.sleep(10)  # Simulate some work
        count += 1
        log_message = f"Fakerunner log {count}"
        print(log_message)  # Print to console (optional)
        send_log(log_message)  # Send log to the web UI

if __name__ == '__main__':
    # Start the web UI in a separate thread
    web_ui_thread = threading.Thread(target=start_web_ui, daemon=True)
    web_ui_thread.start()

    # Run your existing program
    run_program()