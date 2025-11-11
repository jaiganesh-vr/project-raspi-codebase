from picarx import Picarx  
import time

def motor_speed_calibration(self, value):
    """
    Calibrate motor speed difference between left and right motors.

    Args:
        value (list[int, int]): [left_offset, right_offset]
            - left_offset: value to subtract from left motor speed
            - right_offset: value to subtract from right motor speed

    Example:
        px.motor_speed_calibration([5, 0])
        px.motor_speed_calibration([0, -3])
    """
    # Validate input
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("motor_speed_calibration expects a 2-element list [left, right]")

    # Ensure both are integers
    left_offset = int(value[0])
    right_offset = int(value[1])

    # Save calibration offsets
    self.cali_speed_value = [left_offset, right_offset]

    # Optionally store in config file for persistence
    try:
        self.config_flie.set("picarx_speed_calibration", str(self.cali_speed_value))
    except Exception as e:
        print(f"⚠️ Could not save calibration to config: {e}")

    print(f"✅ Motor speed calibration updated: Left={left_offset}, Right={right_offset}")

px = Picarx()

# Left motor is slightly faster → add offset to slow it down
px.motor_speed_calibration([5, 0])

# Test drive
px.forward(50)
time.sleep(2)
px.stop()
