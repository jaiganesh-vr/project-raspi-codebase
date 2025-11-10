from robot_hat.utils import reset_mcu
from picarx import Picarx  
import time

reset_mcu()
time.sleep(0.2)

i = 1
speed = 25

px = Picarx()
actions = ["forward", "right", "straight"]
#actions = ["forward", "reverse", "right", "straight", "left", "straight", "stop"]

try:
    while actions:  # runs while the list is not empty
        print(i)
        current_action = actions.pop(0)  # remove the first item
        if current_action == "forward":
            px.forward(speed)
            time.sleep(5)
            px.stop()
            i += 1
        elif current_action == "reverse":
            px.forward(-25)
            time.sleep(5)
            px.stop()
            i += 1
        elif current_action == "right":
            px.forward(speed)
            for angle in range(0,35,5):
                px.set_dir_servo_angle(angle)
                time.sleep(0.075)
            px.stop()
            i += 1
        elif current_action == "straight":
            px.forward(speed)
            for angle in range(35,0,-5):
                px.set_dir_servo_angle(angle)
                time.sleep(0.075)
            i += 1
        elif current_action == "left":
            px.forward(speed)
            for angle in range(0,-35,-5):
                px.set_dir_servo_angle(angle)
                time.sleep(0.075)
            i += 1
        elif current_action == "stop":
            px.stop()
            i += 1

    print("All actions completed!")
except Exception as e:    
        print("error:%s"%e)
finally:
        px.stop()


