from picarx import Picarx
import time

# === CONFIGURATION ===
SPEED = 50             # Speed (0–100)
ROTATION_TIME = 0.8    # Seconds per wheel rotation (you will calibrate this)
PAUSE = 1.0            # Pause between operations

px = Picarx()

def rotate_wheel(px, wheel='left', rotations=1, speed=SPEED):
    """
    Spins one wheel for an estimated number of rotations.
    This version includes printouts and calibration-friendly timing.
    """
    # Estimated duration per rotation
    duration = rotations * ROTATION_TIME

    # Sanity checks
    wheel = wheel.lower()
    if wheel not in ['left', 'right']:
        raise ValueError("Wheel must be 'left' or 'right'")

    print(f"\n➡️  Rotating {wheel.upper()} wheel: {rotations} rotations (~{duration:.2f}s)")

    # Stop all first (good safety habit)
    px.stop()
    time.sleep(0.2)

    if wheel == 'left':
        px.set_motor_speed(1, speed)   # left wheel
        px.set_motor_speed(2, 0)       # right wheel off
    else:
        px.set_motor_speed(1, 0)
        px.set_motor_speed(2, -speed)  # right wheel (direction may need flipping)

    time.sleep(duration)
    px.stop()
    print(f"✅  {wheel.upper()} wheel stopped.\n")

if __name__ == "__main__":
    try:
        print("Starting rotation test...")
        time.sleep(2)

        # Test left wheel for 2 rotations
        rotate_wheel(px, 'left', rotations=2)
        time.sleep(PAUSE)

        # Test right wheel for 2 rotations
        rotate_wheel(px, 'right', rotations=2)
        time.sleep(PAUSE)

        # Test backwards (optional)
        rotate_wheel(px, 'left', rotations=1, speed=-SPEED)
        rotate_wheel(px, 'right', rotations=1, speed=-SPEED)

    finally:
        px.stop()
        print("Motors stopped safely.")
