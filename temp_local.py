from robot_hat.utils import reset_mcu
from picarx import Picarx

import time

reset_mcu()
time.sleep(2)

TURN_SPEED = 40        # Moderate speed for turning
DRIVE_SPEED = 60       # Normal forward driving speed
TURN_TIME_90 = 1.1     # Seconds to complete a 90° turn (tune this!)
TURN_TIME_180 = 2.2    # Seconds to complete a 180° turn (tune this!)

speed = 1
#actions = ["forward"]
#actions = ["reverse"]
#actions = ["right"]
actions = ["forward", "reverse", "left", "right"]

px = Picarx()

def move_forward(px, duration=1.0, speed=DRIVE_SPEED):
    """
    Move forward for a specified duration.
    """
    px.set_dir_servo_angle(0)
    px.forward(speed)
    time.sleep(duration)
    px.stop()

def turn_left(px, speed=TURN_SPEED):
    """
    Turn the car left by ~90 degrees.
    """
    # Turn wheels left
    px.set_dir_servo_angle(-30)
    # Drive forward briefly to pivot
    px.forward(speed)
    time.sleep(TURN_TIME_90)
    px.stop()
    # Reset steering
    px.set_dir_servo_angle(0)

def turn_right(px, speed=TURN_SPEED):
    """
    Turn the car right by ~90 degrees.
    """
    px.set_dir_servo_angle(30)
    px.forward(speed)
    time.sleep(TURN_TIME_90)
    px.stop()
    px.set_dir_servo_angle(0)

def reverse(px, speed=TURN_SPEED):
    """
    Turn 180 degrees to face the opposite direction.
    """
    px.set_dir_servo_angle(30)   # full right
    px.forward(speed)
    time.sleep(TURN_TIME_180)
    px.stop()
    px.set_dir_servo_angle(0)


if __name__ == "__main__":
    try:
        while actions:
            current_actions = actions.pop(0)
            if current_actions == "forward":
                move_forward(px)
            elif current_actions == "reverse":
                reverse(px)
            elif current_actions == "right":
                turn_right(px)
            elif current_actions == "left":
                turn_left(px)
    finally:
        px.stop()
        time.sleep(0.2)


