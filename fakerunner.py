import argparse
import time
import threading
from cradle.log import Logger, set_verbose
from cradle.monitor import start_web_ui, get_status, set_status, send_stage_update, send_chat_message, send_generic_update, send_skill_library, send_exec_info, send_toolbar,send_image

logger = Logger()
STAGES = ["1 Information Gathering", "2 Self Reflection", "3 Task Inference", "4 Skill Curation", "5 Action Planning"]


def check_status():
    """Check the current status and handle pause/stop behavior."""
    if get_status()=="Stopping":
        print("Program stopped...")
        return False
    elif get_status()=="Pausing":
        set_status("Paused")
        print("Program paused... Waiting to resume.")
        time.sleep(2)
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
        send_stage_update(count,0)
        send_image("C:\\Users\\guoch\\Desktop\\workspace\\FYP\\Cradle\\./runs\\1738342675.471797/screen_1738342904.5611415_augmented.jpg")
        skills = [
            {
                "function_expression": "use_tool()",
                "description": "Executes an in-game action commonly assigned to using the character's current selected tool. According to the selected tool, this action can range from chopping wood using an axe, digging and til soil using a hoe, watering crops using a watering can, breaking stones using a pickaxe, or cutting grass into hay using a scythe. The use of tools is essential for various activities in the game, such as farming, mining, and combat, making this function a versatile and crucial skill for efficient gameplay.",
                "parameters": {}
            },
            {
                "function_expression": "enter_door_and_sleep()",
                "description": "Let the character enter the house and then move the character to the bed and interact with it to go to sleep. This function automates the action of moving the character to the bed and interacting with it to go to sleep.",
                "parameters": {}
            },
            {
                "function_expression": "get_out_of_house()",
                "description": "Move the character out of the house. This function automates the action of moving the character out of the house by navigating through the door.\nNote: This function only takes effect when the character is inside the house and in bed.",
                "parameters": {}
            },
            {
                "function_expression": "do_action()",
                "description": "The function is designed to perform a generic action on objects or characters within one body length of the player character. This could include planting a seed if a seed is selected, harvesting a plant, interacting with other characters, entering doors, opening boxes, or picking up objects. The action is context-specific and depends on what the player is close to in the game environment. This function is essential for progressing through the game, completing quests, and engaging with various interactive elements in the game world, but is limited to only affecting things in very close proximity to the player character.",
                "parameters": {}
            },
            {
                "function_expression": "move_down(duration)",
                "description": "Moves the character downward (south) by pressing the 's' key for the specified duration. This action simulates the character moving down on the game grid, allowing for precise control over the character's position and orientation.\nNote: The movement distance is influenced by the duration of the key press, with a typical rate of approximately 1 grid space per 0.1 seconds of key press. Understanding this relationship is essential for strategic navigation and precise positioning within the game environment.\n\nParameters:\n - duration: The duration in seconds for which the 's' key should be pressed, determining the distance the character will move backward (default is 0.1 second).",
                "parameters": {
                    "duration": "The duration in seconds for which the 's' key should be pressed, determining the distance the character will move backward (default is 0.1 second)"
                }
            },
            {
                "function_expression": "move_up(duration)",
                "description": "Moves the character upward (north) by pressing the 'w' key for the specified duration. This action simulates the character moving up on the game grid, allowing for precise control over the character's position and orientation.\nNote: The movement distance is influenced by the duration of the key press, with a typical rate of approximately 1 grid space per 0.1 seconds of key press. Understanding this relationship is essential for strategic navigation and precise positioning within the game environment.\n\nParameters:\n - duration: The duration in seconds for which the 'w' key should be pressed, determining the distance the character will move forward (default is 0.1 second).",
                "parameters": {
                    "duration": "The duration in seconds for which the 'w' key should be pressed, determining the distance the character will move forward (default is 0.1 second)"
                }
            },
            {
                "function_expression": "move_left(duration)",
                "description": "Moves the character to the left (west) by pressing the 'a' key for the specified duration. This action simulates the character moving left on the game grid, allowing for precise control over the character's position and orientation.\nNote: The movement distance is influenced by the duration of the key press, with a typical rate of approximately 1 grid space per 0.1 seconds of key press. Understanding this relationship is essential for strategic navigation and precise positioning within the game environment (default is 0.1 second).\n\nParameters:\n - duration: The duration in seconds for which the 'a' key should be pressed, determining the distance the character will move to the left (default is 0.1 second).",
                "parameters": {
                    "duration": "The duration in seconds for which the 'a' key should be pressed, determining the distance the character will move to the left (default is 0.1 second)"
                }
            },
            {
                "function_expression": "move_right(duration)",
                "description": "Moves the character to the right (east) by pressing the 'd' key for the specified duration. This action simulates the character moving right on the game grid, allowing for precise control over the character's position and orientation.\nNote: The movement distance is influenced by the duration of the key press, with a typical rate of approximately 1 grid space per 0.1 seconds of key press. Understanding this relationship is essential for strategic navigation and precise positioning within the game environment (default is 0.1 second).\n\nParameters:\n - duration: The duration in seconds for which the 'd' key should be pressed, determining the distance the character will move to the right (default is 0.1 second).",
                "parameters": {
                    "duration": "The duration in seconds for which the 'd' key should be pressed, determining the distance the character will move to the right (default is 0.1 second)"
                }
            },
            {
                "function_expression": "select_tool(key)",
                "description": "Selects a specific tool from the in-game toolbar based on the given tool number. Each tool serves a distinct purpose essential for managing your farm and exploring the world. This function allows for the quick selection of tools, crucial for efficient gameplay during various in-game activities such as farming, mining, or combat.\nNote: Ensure the tool number is within the valid range to prevent errors. This function is essential for efficiently managing tool use in various game scenarios, enabling the player to swiftly switch between tools as the situation demands.\n\nParameters:\n - key: A key representing the position of the tool in the toolbar. The value must be in [\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"8\",\"9\",\"0\",\"-\",\"+\"], inclusive.",
                "parameters": {
                    "key": "A key representing the position of the tool in the toolbar. The value must be in [\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"8\",\"9\",\"0\",\"-\",\"+\"], inclusive"
                }
            }
        ]
        send_skill_library(skills)
        send_generic_update('action',"get_out_of_house()")
        logger.write(f"Fakerunner log {count}")  # Call to logger
        send_generic_update("task_description",f"Iteration {count}: The ground of the farm below the home is now scattered with various obstacles, including rocks, woods, trees, grasses and weeds. Get out of the house and move down and clear each obstacle one by one near the house.")
        send_generic_update("subtask_description",f"Iteration {count}: The current subtask is to continue chopping down the tree near the house using the axe.")
        time.sleep(5)
        send_stage_update(count,1)
        send_exec_info({
            "executed_skills": [
                "get_out_of_house()"
            ],
            "last_skill": "get_out_of_house()",
            "errors": False,
            "errors_info": ""
        })
        time.sleep(2)
        tbl = [
            {
                "name": "axe",
                "number": 1,
                "position": 1
            },
            {
                "name": "hoe",
                "number": 1,
                "position": 2
            },
            {
                "name": "full_watering_can",
                "number": 1,
                "position": 3
            },
            {
                "name": "pickaxe",
                "number": 1,
                "position": 4
            },
            {
                "name": "scythe",
                "number": 1,
                "position": 5
            },
            {
                "name": "fiber",
                "number": 36,
                "position": 6
            },
            {
                "name": "stone",
                "number": 21,
                "position": 7
            },
            {
                "name": "wood",
                "number": 99,
                "position": 8
            },
            {
                "name": "sap",
                "number": 27,
                "position": 9
            },
            {
                "name": "stone",
                "number": 1,
                "position": 10
            },
            {
                "name": "blank",
                "number": 1,
                "position": 11
            },
            {
                "name": "stone",
                "number": 1,
                "position": 12
            }
        ]
        tb = {
            "toolbar": tbl,
            "selected_position": 1,
        }
        send_toolbar(tb)
        send_stage_update(count,2)
        send_chat_message("Cradle", "Hello! I'm Cradle. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        send_chat_message("GPT-4o", "Hi Cradle! How can I help? Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

        if not check_status():
            break

        warn_message = f"This is a fucking warning {count}"
        logger.warn(warn_message)  # Call to logger
        send_generic_update('action',"use_tool()")
        send_generic_update('summarization',"The summary is on Sat. 13, the character woke up and got out of bed. The character is now standing next to the bed, ready to move out of the house to start clearing obstacles.")
        time.sleep(3)  # Simulate some work
        send_stage_update(count,3)
        thing = {
  "date_time": "Sat. 13, 6:10 am",
  "energy": "270/270",
  "weather": "Sunny",
  "dialog": "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
  "other": "Ut enim ad minim veniam, quis nostrud exercitation..."
}
        send_generic_update("game_status", thing)
        time.sleep(3)  # Simulate some work
        send_stage_update(count,4)
        send_exec_info({
            "executed_skills": [
                "use_tool()"
            ],
            "last_skill": "use_tool()",
            "errors": False,
            "errors_info": ""
        })
        time.sleep(3)  # Simulate some work

        if not check_status():
            break


def get_args_parser():

    parser = argparse.ArgumentParser("Cradle Agent Runner")
    parser.add_argument("--verbose", type=int, choices=[1, 2, 3, 4], default=1, help="Set the verbose level for cradle monitor: 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG")
    return parser

if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    set_verbose(args.verbose)
    
    # Start the web UI in a separate thread
    web_ui_thread = threading.Thread(target=start_web_ui, daemon=True)
    web_ui_thread.start()

    # Run your existing program
    run_program()