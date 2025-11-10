# navigator.py
import time
from typing import List
from math import copysign

# thresholds (tweak for your robot & environment)
OBSTACLE_DISTANCE_CM = 30     # anything closer is an obstacle
DEADEND_CHECK_SAMPLES = 3     # number of grayscale samples to check for cliff
STEERING_ANGLE = 20           # degrees for quick left/right turns
MANEUVER_DURATION = 0.4       # seconds to run short moves
RACE_SPEED_BONUS = 20         # extra speed when upshifted

class Navigator:
    """
    Navigator translates high-level manoeuvre strings into Picarx hardware calls.
    It also uses sensors to label the environment as "Clear", "Obstacle", "DeadEnd".
    """
    def __init__(self, px):
        self.px = px
        # ensure centered steering
        try:
            self.px.set_dir_servo_angle(0)
        except Exception as e:
            print("[Navigator] Warning setting initial steer angle:", e)

    def _get_sensor_state(self):
        """
        Return one of: "Clear", "Obstacle", "DeadEnd"
        - Obstacle: ultrasonic distance below threshold
        - DeadEnd: grayscale cliff_flag true (uses get_cliff_status)
        """
        try:
            dist = self.px.get_distance()  # centimeters (assumes Ultrasonic.read returns cm)
        except Exception as e:
            print("[Navigator] ultrasonic read error:", e)
            dist = None

        try:
            gm = self.px.get_grayscale_data()
        except Exception as e:
            print("[Navigator] grayscale read error:", e)
            gm = None

        # Dead end takes priority (cliff)
        if gm is not None:
            if self.px.get_cliff_status(gm):
                return "DeadEnd"
        # Then obstacle
        if dist is not None and dist > 0 and dist < OBSTACLE_DISTANCE_CM:
            return "Obstacle"
        return "Clear"

    def manoeuvre(self, action: str, speed: int = 50, gear: int = 1) -> bool:
        """
        Execute one of the manoeuvres:
        Start, Forward, Right, Left, Reverse, Upshift, Downshift, Stop

        Returns True if completed normally, False if an emergency stop was triggered.
        """
        action = action.strip().capitalize()
        # apply gear modifier to speed
        actual_speed = int(speed + (gear - 1) * RACE_SPEED_BONUS)
        actual_speed = max(0, min(100, actual_speed))
        sensor_state = self._get_sensor_state()
        print(f"[Navigator] Sensor state: {sensor_state} | executing {action} @ {actual_speed}%")

        # emergency behaviours
        if sensor_state == "DeadEnd":
            print("[Navigator] DEAD END detected! Immediate reverse and stop.")
            # reverse a small amount, then stop and abort further actions
            self._do_reverse(actual_speed, duration=0.5)
            self.px.stop()
            return False   # signal abort of plan
        if sensor_state == "Obstacle" and action in ("Forward", "Start"):
            # evasive: small steer + short backup then continue
            print("[Navigator] Obstacle detected during forward/start -> evasive turn")
            self._do_turn(STEERING_ANGLE, duration=0.25)   # quick turn right
            self._do_forward(actual_speed, duration=MANEUVER_DURATION)
            return True

        # action dispatch
        if action == "Start":
            # calibrate or just set a tiny torque to awaken motors
            self.px.set_dir_servo_angle(0)
            self.px.set_power(0)
            time.sleep(0.05)
            return True
        elif action == "Forward":
            self._do_forward(actual_speed, duration=MANEUVER_DURATION)
            return True
        elif action == "Right":
            self._do_turn(-STEERING_ANGLE, actual_speed)   # negative to turn right (servo sign may vary)
            return True
        elif action == "Left":
            self._do_turn(STEERING_ANGLE, actual_speed)
            return True
        elif action == "Reverse":
            self._do_reverse(actual_speed, duration=MANEUVER_DURATION)
            return True
        elif action == "Upshift":
            # caller (Driver) should keep track of gear; return True to continue
            print("[Navigator] Upshift: nothing to do at hardware level (Driver should adjust gear).")
            return True
        elif action == "Downshift":
            print("[Navigator] Downshift: nothing to do at hardware level (Driver should adjust gear).")
            return True
        elif action == "Stop":
            self.px.stop()
            time.sleep(0.05)
            return True
        else:
            print(f"[Navigator] Unknown action '{action}'. Ignored.")
            return True

    # ----- helper low level motion wrappers -----
    def _do_forward(self, speed: int, duration: float = 0.4):
        # drive forward for duration (non-blocking safety: always check sensors at start)
        self.px.set_dir_servo_angle(0)  # center wheels for straight line
        print(f"[Navigator] forward @ {speed}% for {duration}s")
        self.px.forward(speed)
        time.sleep(duration)
        self.px.stop()

    def _do_reverse(self, speed: int, duration: float = 0.4):
        self.px.set_dir_servo_angle(0)
        print(f"[Navigator] reverse @ {speed}% for {duration}s")
        self.px.backward(speed)
        time.sleep(duration)
        self.px.stop()

    def _do_turn(self, angle: int, speed: int = 40, duration: float = 0.55):
        # angle in degrees: positive = left, negative = right
        angle = int(max(-30, min(30, angle)))
        print(f"[Navigator] turning to angle {angle}°, moving @ {speed}% for {duration}s")
        self.px.set_dir_servo_angle(angle)
        # move a little while steering to execute arc
        self.px.forward(speed)
        time.sleep(duration)
        self.px.stop()
        # re-center
        self.px.set_dir_servo_angle(0)
        time.sleep(0.05)
