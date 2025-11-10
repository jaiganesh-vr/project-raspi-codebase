from robot_hat.utils import reset_mcu
from picarx import Picarx

import time

reset_mcu()
time.sleep(2)

speed = 0.001
#actions = ["forward"]
#actions = ["reverse"]
#actions = ["right"]
actions = ["left"]

px = Picarx()

def move_forward(speed):
    px.forward(speed)
    time.sleep(1)
    px.stop

def move_right(speed):
    for angle in range(0, 50, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075)
    px.forward(speed)
    time.sleep(0.25)
    px.stop()
    for angle in range(50, 0, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075)

def move_left(speed):
    for angle in range(0, -50, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075)
    px.forward(speed)
    time.sleep(0.25)
    px.stop()
    px.set_dir_server(-45)
    px.forward(speed)
    time.sleep(0.25)
    px.stop()
    for angle in range(-50, 0, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075) 
    px.set_dir_server(0)

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


