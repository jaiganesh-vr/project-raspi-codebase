# motor_calibration.py
import time
from picarx import Picarx

def calibrate_motor_speed(px: Picarx):
    """
    Interactive motor speed calibration.
    Adjust until the robot moves straight forward.
    """
    print("🧭 Motor Speed Calibration")
    print("--------------------------")
    print("This will make the car move forward slowly for testing.")
    print("Use adjustments until it moves straight.\n")

    # Initial calibration values (difference between left & right)
    cali_left = 0
    cali_right = 0
    base_speed = 50

    try:
        while True:
            print(f"\nCurrent calibration: left={cali_left}, right={cali_right}")
            px.motor_speed_calibration([cali_left, cali_right])
            px.forward(base_speed)
            time.sleep(2)
            px.stop()

            action = input("Adjust (l/r to tweak, s to save, q to quit): ").lower()

            if action == "l":
                cali_left += int(input("Enter new offset for LEFT motor (+/-): "))
            elif action == "r":
                cali_right += int(input("Enter new offset for RIGHT motor (+/-): "))
            elif action == "s":
                px.motor_speed_calibration([cali_left, cali_right])
                px.config_flie.set("motor_speed_calibration", f"[{cali_left}, {cali_right}]")
                print("✅ Calibration saved.")
            elif action == "q":
                print("Exiting calibration.")
                break
            else:
                print("Unknown command. Use: l/r/s/q")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nCalibration interrupted.")
    finally:
        px.stop()

if __name__ == "__main__":
    px = Picarx()
    calibrate_motor_speed(px)
