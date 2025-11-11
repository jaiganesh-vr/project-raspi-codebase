from robot_hat.utils import reset_mcu
from picarx import Picarx  
import time

# --- Initialization ---
i = 1
reset_mcu()
time.sleep(2)
start = (3, 3) 
facing = "up"
px = Picarx()

# --- Constants ---
TURN_SPEED = 10         # Moderate speed for turning
TURN_TIME_LEFT = 1.6      # Seconds to complete a 90° turn

# --- Movement Functions ---

def turn_left(px, speed=TURN_SPEED):
    """Turn the car left by ~90 degrees."""

    px.set_motor_speed(1, 0)       # left wheel stopped
    px.set_motor_speed(2, -speed) 
    for angle in range(0, -35, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.25)
    time.sleep(0.25)    
    px.stop()
    for angle in range(-32, 2, 2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)   

def turn_right(px, speed=TURN_SPEED):
    """Turn the car left by ~90 degrees."""

    px.set_motor_speed(1, speed)       # left wheel stopped
    px.set_motor_speed(2, 0) 
    for angle in range(0, 35, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    time.sleep(0.25)    
    px.stop()
    for angle in range(32, 0, 2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)   

actions = ["right"]

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
        
except Exception as e:    
        print("error:%s"%e)
finally:
        px.stop()
        reset_mcu()
        time.sleep(1)


