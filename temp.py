from picarx import Picarx
import time


if __name__ == "__main__":
    try:
        # init picarx
        px = Picarx()

        for angle in range(0, 35, 2):
            px.set_dir_servo_angle(angle)
            time.sleep(1)
        for angle in range(35, -35, -1):
            px.set_dir_servo_angle(angle)
            time.sleep(1)
        for angle in range(-35, 0, 2):
            px.set_dir_servo_angle(angle)
            time.sleep(1)

    finally:
        px.stop()
        time.sleep(0.2)


