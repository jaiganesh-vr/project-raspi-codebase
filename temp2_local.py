from picarx import Picarx
import time

# === Constants ===
SPEED = 50            # Motor speed (0–100)
ROTATION_TIME = 0.7   # Approx time (in seconds) for one full wheel rotation at SPEED
                      # <-- You’ll need to measure & tune this value manually

px = Picarx()

def rotate_wheel(px, wheel='left', rotations=1, speed=SPEED):
    """
    Spins a specified wheel for a certain number of rotations.
    Since Picar-X lacks encoders, this uses a time estimate.
    """
    duration = rotations * ROTATION_TIME
    print(f"Rotating {wheel} wheel for {rotations} rotations (~{duration:.2f}s)...")

    # Choose which wheel to activate
    if wheel.lower() == 'left':
        px.set_motor_speed(1, speed)
        px.set_motor_speed(2, 0)
    elif wheel.lower() == 'right':
        px.set_motor_speed(1, 0)
        px.set_motor_speed(2, -speed)  # adjust sign if reversed
    else:
        raise ValueError("Wheel must be 'left' or 'right'")

    time.sleep(duration)
    px.stop()


if __name__ == "__main__":
    try:
        # Example: make the left wheel rotate twice, then the right wheel once
        rotate_wheel(px, 'left', rotations=2)
        time.sleep(1)
        rotate_wheel(px, 'right', rotations=1)
    finally:
        px.stop()
        print("Motors stopped.")
