from robot_hat.utils import reset_mcu
from picarx import Picarx
import time

# --- Initialization ---
reset_mcu()
time.sleep(2)
px = Picarx()

# --- Constants ---
TURN_SPEED = 40         # Moderate speed for turning
DRIVE_SPEED = 60        # Normal forward driving speed
TURN_TIME_RIGHT = 1.30      # Seconds to complete a 90° turn
TURN_TIME_LEFT = 2.45      # Seconds to complete a 90° turn
TURN_TIME_180 = 2.2     # Seconds to complete a 180° turn
PAUSE_BETWEEN_ACTIONS = 1.5  # Seconds to pause after each action

# --- Action List ---
#actions = ["forward", "reverse", "left", "right"]
actions = ["left"]
#actions = ["right", "right", "right", "right"]


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


# --- Main Execution Loop ---
if __name__ == "__main__":
    try:
        while actions:
            current_action = actions.pop(0)
            print(f"Executing: {current_action}")

            if current_action == "forward":
                move_forward(px)
            elif current_action == "reverse":
                reverse(px)
            elif current_action == "right":
                turn_right(px)
            elif current_action == "left":
                turn_left(px)

            # Pause between steps
            print(f"Pausing for {PAUSE_BETWEEN_ACTIONS} seconds...\n")
            px.stop()
            time.sleep(PAUSE_BETWEEN_ACTIONS)

    finally:
        print("Stopping motors and resetting.")
        px.stop()
        time.sleep(0.5)
