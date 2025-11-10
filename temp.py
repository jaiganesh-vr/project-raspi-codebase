from picarx import Picarx
import time


if __name__ == "__main__":
    try:
        # init picarx
        px = Picarx()

        px.forward(50)
        time.sleep(5)
        px.stop()


        px.forward(-50)
        time.sleep(5)
        px.stop()

        px.set_dir_servo_angle(35)
        time.sleep(5)
        px.set_dir_servo_angle(-35)
        time.sleep(5)
        px.set_dir_servo_angle(0)
        time.sleep(5)


    finally:
        px.stop()
        time.sleep(0.2)


