from robot_hat.utils import reset_mcu
from picarx import Picarx  
import time

reset_mcu()
time.sleep(0.2)

i = 1
speed = 25

px = Picarx()

actions = ["forward", "reverse", "right", "straight", "left",  "stop"]

try:
    while actions:  # runs while the list is not empty
        print(i)
        current_action = actions.pop(0)  # remove the first item
        if current_action == "forward":
            px.forward(speed)
            time.sleep(1)
            px.stop()
            i += 1
        elif current_action == "reverse":
            px.forward(-25)
            time.sleep(1)
            px.stop()
            i += 1
        elif current_action == "right":
            for angle in range(0,35,5):
                 px.set_dir_servo_angle(angle)
            time.sleep(1)
            px.stop()
            i += 1
        elif current_action == "straight":
            for angle in range(0,35,5):
                px.set_dir_servo_angle(angle)
                time.sleep(0.25)
            i += 1
        elif current_action == "left":
            for angle in range(0,-35,5):
                px.set_dir_servo_angle(angle)
                time.sleep(0.25)
            i += 1
        elif current_action == "stop":
            px.stop()
            i += 1

    print("All actions completed!")
except Exception as e:    
        print("error:%s"%e)
finally:
        px.stop()


