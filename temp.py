from picarx import Picarx
import time


if __name__ == "__main__":
    try:
        # init picarx
        px = Picarx()

        for x in range(0,100,10):
            px.forward(x)
            print(x)
            time.sleep(2)

        for x in range(0,-100,10):
            px.forward(x)
            print(x)
            time.sleep(2)

        for angle in range(0, 35, 2.5):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)
        for angle in range(35, -35, -1):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)
        for angle in range(-35, 0, 2.5):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)

    finally:
        px.stop()
        time.sleep(0.2)


