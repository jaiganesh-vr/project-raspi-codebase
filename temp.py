from picarx import Picarx
import time


if __name__ == "__main__":
    try:
        # init picarx
        px = Picarx()

        for angle in range(0, 35, 5):
            px.set_dir_servo_angle(angle)
            time.sleep(0.5)
        for angle in range(35, -35, 5):
            px.set_dir_servo_angle(angle)
            time.sleep(0.5)
        for angle in range(-35, 0, 5):
            px.set_dir_servo_angle(angle)
            time.sleep(0.5)

    finally:
        px.stop()
        time.sleep(0.2)


