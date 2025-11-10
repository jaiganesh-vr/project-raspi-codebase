from robot_hat.utils import reset_mcu
from picarx import Picarx

import time

reset_mcu()
time.sleep(2)

speed = 1
#actions = ["forward"]
#actions = ["reverse"]
#actions = ["right"]
actions = ["left", "forward", "right", "forward"]

px = Picarx()

def move_forward(speed):
    print("Driving Forward")
    px.forward(speed)
    time.sleep(1)
    px.stop

def move_right(speed):
    print("Steering Right")
    for angle in range(0, 50, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075)
    px.forward(speed)
    time.sleep(1)
    px.stop()
    for angle in range(50, 0, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075)
    px.set_dir_servo_angle(0)
    print("Unsteering right")

def move_left(speed):
    print("Steering Left")
    for angle in range(0, -50, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075)
    px.forward(speed)
    time.sleep(2.25)
    px.stop()
    for angle in range(-50, 0, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075) 
    px.set_dir_servo_angle(0)
    print("Unsteering Left")


if __name__ == "__main__":
    try:
        while actions:
            current_actions = actions.pop(0)
            if current_actions == "forward":
                move_forward(speed)
            elif current_actions == "reverse":
                move_reverse(speed)
            elif current_actions == "right":
                move_right(speed)
            elif current_actions == "left":
                move_left(speed)
    finally:
        px.stop()
        time.sleep(0.2)


