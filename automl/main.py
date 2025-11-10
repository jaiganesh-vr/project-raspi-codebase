from robot_hat.utils import reset_mcu
from picarx import Picarx  
import navigator
import time

# --- Initialization ---
i = 1
reset_mcu()
time.sleep(2)
speed = 0.001
start = (5, 5) 
facing = "up"
px = Picarx()

# --- Constants ---
TURN_SPEED = 40         # Moderate speed for turning
DRIVE_SPEED = 60        # Normal forward driving speed
TURN_TIME_RIGHT = 1.30      # Seconds to complete a 90° turn
TURN_TIME_LEFT = 2.65      # Seconds to complete a 90° turn
TURN_TIME_180 = 2.2     # Seconds to complete a 180° turn
PAUSE_BETWEEN_ACTIONS = 1.5  # Seconds to pause after each action

# --- Movement Functions ---
def move_forward(px, duration=1.0, speed=DRIVE_SPEED):
    """Move forward for a specified duration."""
    px.set_dir_servo_angle(0)
    px.forward(speed)
    time.sleep(duration)
    px.stop()


def turn_left(px, speed=TURN_SPEED):
    """Turn the car left by ~90 degrees."""
    px.set_dir_servo_angle(-22)
    time.sleep(0.25)
    px.forward(10)
    time.sleep(TURN_TIME_LEFT)
    px.stop()
    px.set_dir_servo_angle(0)


def turn_right(px, speed=TURN_SPEED):
    """Turn the car right by ~90 degrees."""
    px.set_dir_servo_angle(30)
    px.forward(speed)
    time.sleep(TURN_TIME_RIGHT)
    px.stop()
    px.set_dir_servo_angle(0)


def reverse(px, speed=TURN_SPEED):
    """Turn 180 degrees to face the opposite direction."""
    px.set_dir_servo_angle(30)   # full right
    px.forward(speed)
    time.sleep(TURN_TIME_180)
    px.stop()
    px.set_dir_servo_angle(0)


actions = ["left"]
#actions = ["forward", "reverse", "right", "straight", "left", "straight", "stop"]

try:
    while actions:  # runs while the list is not empty
        current_action = actions.pop(0)  # remove the first item
        print(f"Executing: {1,"-",current_action}")
        if current_action == "forward":
            move_forward(px)
            i += 1
        elif current_action == "reverse":
            reverse(px)
            i += 1
        elif current_action == "right":
            turn_right(px)
            i += 1
        elif current_action == "straight":
            turn_left(px)
            i += 1
        elif current_action == "left":
            px.forward(speed)
            for angle in range(0,-35,-5):
                px.set_dir_servo_angle(angle)
                time.sleep(0.075)
            i += 1
        elif current_action == "stop":
            px.stop()
            i += 1
        elif current_action == "end":
            grid = navigator.load_map("map.txt")  
            print(start)    
            goal = navigator.generate_random_goal(grid,start)
            path = navigator.find_shortest_path(grid, start, goal)
            if path:
                print("Path found:", path)
                directions = navigator.path_to_directions(path)
                print(directions)
                relative_direction,facing = navigator.convert_absolute_to_relative(directions,facing)
                actions.extend(relative_direction)
                print("Directions:", relative_direction,facing)
                actions.append("end")
            else:
                print("No path found.")
            start = goal
            print(start)
    print("All actions completed!")
except Exception as e:    
        print("error:%s"%e)
finally:
        px.stop()


