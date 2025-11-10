from picarx import Picarx   # your hardware file (the big class you pasted)
import time

speed = 25
px = Picarx()

actions = ["forward", "left", "right", "reverse"]

while actions:  # runs while the list is not empty
    current_action = actions.pop(0)  # remove the first item
    if current_action == "forward":
        px.forward(speed)
        time.sleep(5)
        px.stop
    elif current_action == "left":
        for angle in range(0,35,10):
            px.set_dir_servo_angle(angle)
        px.forward(speed)
        time.sleep(5)
        px.stop
    elif current_action == "right":
        for angle in range(0,35,10):
            px.set_dir_servo_angle(angle)
        px.forward(speed)
        time.sleep(5)
        px.stop
    elif current_action == "reverse":
        px.forward(-25)
    time.sleep(5)

print("All actions completed!")
