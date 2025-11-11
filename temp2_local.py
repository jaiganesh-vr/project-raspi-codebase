from picarx import Picarx
import time

# --- Constants ---
SPEED = 50          # Speed for active wheel
DURATION = 1.5      # How long to run each wheel (seconds)

# --- Initialize the Picar-X ---
px = Picarx()

def turn_left_wheel(px, speed=SPEED, duration=DURATION):
    """
    Spins only the left wheel.
    Positive speed moves it forward; negative speed moves it backward.
    """
    print("Spinning LEFT wheel...")
    px.set_motor_speed(1, speed)   # left wheel active
    px.set_motor_speed(2, 0)       # right wheel stopped
    time.sleep(duration)
    px.stop()

def turn_right_wheel(px, speed=SPEED, duration=DURATION):
    """
    Spins only the right wheel.
    Positive speed moves it forward; negative speed moves it backward.
    """
    print("Spinning RIGHT wheel...")
    px.set_motor_speed(1, 0)       # left wheel stopped
    px.set_motor_speed(2, -speed)  # right wheel active (negative flips direction)
    time.sleep(duration)
    px.stop()

if __name__ == "__main__":
    try:
        # Example: spin each wheel forward, then backward
        turn_left_wheel(px, SPEED)
        time.sleep(1)
        turn_right_wheel(px, SPEED)
        time.sleep(1)
        turn_left_wheel(px, -SPEED)
        time.sleep(1)
        turn_right_wheel(px, -SPEED)

    finally:
        px.stop()
        print("Motors stopped safely.")
