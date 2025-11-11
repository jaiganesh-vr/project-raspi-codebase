from robot_hat.utils import reset_mcu
from picarx import Picarx  
import navigator
import time

# --- Initialization ---
i = 1
reset_mcu()
time.sleep(2)
start = (5, 5) 
facing = "up"
px = Picarx()

# --- Constants ---
TURN_SPEED = 30         # Moderate speed for turning
DRIVE_SPEED = 30        # Normal forward driving speed
TURN_TIME_RIGHT = 2      # Seconds to complete a 90° turn
TURN_TIME_LEFT = 1.5      # Seconds to complete a 90° turn
TURN_TIME_180 = 3     # Seconds to complete a 180° turn
PAUSE_BETWEEN_ACTIONS = 1  # Seconds to pause after each action

# --- Movement Functions ---
def move_forward(px, duration=1.0, speed=DRIVE_SPEED):
    """Move forward for a specified duration."""
    px.set_dir_servo_angle(0)
    px.forward(speed)
    time.sleep(duration)
    px.stop()

def turn_left(px, speed=TURN_SPEED):
    """Turn the car left by ~90 degrees."""
    for angle in range(0, -32, -2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.1)
    px.set_motor_speed(1, 0)       # left wheel stopped
    px.set_motor_speed(2, -speed) 
    time.sleep(TURN_TIME_LEFT)
    px.stop()
    for angle in range(-32, 6, 2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.1)

def turn_right(px, speed=TURN_SPEED):
    """Turn the car right by ~90 degrees."""
    for angle in range(0, 32, 2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.1)    
    px.set_motor_speed(1, speed)   # left wheel active
    px.set_motor_speed(2, 0)      
    time.sleep(TURN_TIME_RIGHT)
    px.stop()
    for angle in range(32, 0, -2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.1)   

def reverse(px, speed=TURN_SPEED):
    """Turn 180 degrees to face the opposite direction."""
    for angle in range(0, 32, 2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.1)       
    px.set_motor_speed(1, speed)   # left wheel active
    px.set_motor_speed(2, 0)     
    time.sleep(TURN_TIME_180)
    px.stop()
    for angle in range(32, 0, -2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.1)   

actions = ["reverse"]
#actions = ["left", "right", "reverse","forward"]
#actions = ["forward", "reverse", "right", "straight", "left", "straight", "stop"]

try:
    while actions:  # runs while the list is not empty
        current_action = actions.pop(0)  # remove the first item
        print(f"Executing: {current_action}")
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
            turn_left(px)
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
        
         # Pause between steps
        print(f"Pausing for {PAUSE_BETWEEN_ACTIONS} seconds...\n")
        px.stop()
        time.sleep(PAUSE_BETWEEN_ACTIONS)
    print("All actions completed!")
except Exception as e:    
        print("error:%s"%e)
finally:
        px.stop()
        reset_mcu()
        time.sleep(1)


