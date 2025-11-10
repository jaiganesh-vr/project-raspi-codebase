from robot_hat.utils import reset_mcu
from picarx import Picarx  
import navigator
import time

reset_mcu()
time.sleep(2)

i = 1
speed = 10
start = (5, 5) 

px = Picarx()

actions = ["forward", "reverse", "right", "straight", "left", "straight", "stop","end"]

try:
    while actions:  # runs while the list is not empty
        print(i)
        current_action = actions.pop(0)  # remove the first item
        if current_action == "forward":
            px.forward(speed)
            time.sleep(2)
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
            for angle in range(35,-5,-5):
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
        elif current_action == "end":
            grid = navigator.load_map("map.txt")      
            goal = navigator.generate_random_goal(grid,start)   # bottom-right
            path = navigator.find_shortest_path(grid, start, goal)
            if path:
                print("Path found:", path)
                directions = navigator.path_to_directions(path)
                actions.append(directions)
                print("Directions:", directions)
                start == goal
            else:
                print("No path found.")
    print("All actions completed!")
except Exception as e:    
        print("error:%s"%e)
finally:
        px.stop()


