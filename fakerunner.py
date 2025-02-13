import time
import threading
from cradle.log import Logger
from cradle.monitor import start_web_ui

logger = Logger()

def run_program():
    """Your existing program logic."""
    count = 0
    while True:
        time.sleep(5)  # Simulate some work
        count += 1
        write_message = f"Fakerunner log {count}"
        print(write_message)  # Print to console (optional)
        logger.write(write_message)  # Call to logger
        warn_message = f"This is a fucking warning {count}"
        print(warn_message)
        logger.warn(warn_message)  # Call to logger


if __name__ == '__main__':
    # Start the web UI in a separate thread
    web_ui_thread = threading.Thread(target=start_web_ui, daemon=True)
    web_ui_thread.start()

    # Run your existing program
    run_program()