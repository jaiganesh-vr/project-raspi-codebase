from picarx import Picarx
import time

speed = 0.001
actions = ["reverse"]

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
    time.sleep(1.25)
    for angle in range(40, 0, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.075)
    px.stop 

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


