from picarx import Picarx   # your hardware file (the big class you pasted)
import time

i = 1
speed = 25
px = Picarx()

actions = ["forward", "left", "right", "reverse", "stop"]

try:
    while actions:  # runs while the list is not empty
        print(i)
        current_action = actions.pop(0)  # remove the first item
        if current_action == "forward":
            px.forward(speed)
            time.sleep(1)
            px.stop()
            i += 1
        elif current_action == "left":
            px.set_dir_servo_angle(-30)
            time.sleep(1)
            px.stop()
            i += 1
        elif current_action == "right":
            px.set_dir_servo_angle(30)
            time.sleep(1)
            px.stop()
            i += 1       
        elif current_action == "reverse":
            px.forward(-25)
            time.sleep(1)
            i += 1
        elif current_action == "stop":
            px.stop()
            i += 1

    print("All actions completed!")
except Exception as e:    
        print("error:%s"%e)
finally:
        px.stop()


