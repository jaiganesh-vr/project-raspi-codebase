from robot_hat.utils import reset_mcu
from vilib import Vilib
import navigator
import readchar
import time

# --- Initialization ---
reset_mcu()
time.sleep(2)

# --- Constants ---
TURN_SPEED = 10         # Moderate speed for turning
DRIVE_SPEED = 10        # Normal forward driving speed
PAUSE_BETWEEN_ACTIONS = 0  # Seconds to pause after each action

# --- Helper Functions ---
def constrain(x, min_val, max_val):
    return max(min_val, min(max_val, x))

# --- Manual Movement Functions ---
def engine_start(px):
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1*10) 

def engine_stop(px):
    px.stop()

def engine_reverse(px):
    px.set_motor_speed(1, -1*10)
    px.set_motor_speed(2, 10)  

def steer_left(px,current_angle):
    temp_angle = current_angle
    new_angle = temp_angle - 5
    final_angle = constrain(new_angle,-30,30)
    for x in range(current_angle,final_angle+1, -1):
        px.set_dir_servo_angle(x)
        time.sleep(0.0125)
    return final_angle

def steer_center(px,current_angle):
    if current_angle >= 0:
        for x in range(current_angle, 1, -1):
            px.set_dir_servo_angle(x)
            time.sleep(0.0125)
    else:
        for x in range(current_angle, 1, 1):
            px.set_dir_servo_angle(x)
            time.sleep(0.0125)
    return 0

def steer_right(px,current_angle):
    temp_angle = current_angle
    new_angle = temp_angle + 5
    final_angle = constrain(new_angle,-30,30)
    for x in range(current_angle,final_angle+1, 1):
        px.set_dir_servo_angle(x)
        time.sleep(0.0125)
    return final_angle

# --- Auto Movement Functions ---

def move_forward(px, duration=1.0, speed=DRIVE_SPEED):
    px.set_dir_servo_angle(0)
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1*10)     
    time.sleep(duration)
    px.stop()

def move_reverse(px, speed=TURN_SPEED):
    for angle in range(0, 35, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    px.set_motor_speed(1, speed)   
    px.set_motor_speed(2, 0)  
    time.sleep(1.350)
    px.stop()
    for angle in range(30, 0, -2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)  

def turn_left(px, speed=TURN_SPEED):
    #Steering turns left
    for angle in range(0, -35, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    #Right motor moves forward
    px.set_motor_speed(1, 0)       
    px.set_motor_speed(2, -1*speed)     
    time.sleep(0.85)    
    px.stop()
    #Steering sets back to zero   
    for angle in range(-35, 5, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    #Steering moves right    
    for angle in range(0, 40, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    px.set_motor_speed(1, -1*speed)       
    px.set_motor_speed(2, 0)
    time.sleep(0.5) 
    for angle in range(30, -5, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)    
       
def turn_right(px, speed=TURN_SPEED):
    #Steering turns right
    for angle in range(0, 35, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    #Left motor move forward
    px.set_motor_speed(1, speed) 
    px.set_motor_speed(2, 0)   
    time.sleep(0.5)
    px.stop()
    #Steering sets back to zero
    for angle in range(30, -5, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525) 
    #Steering turns left
    for angle in range(0, -35, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)  
    #Right motor moves backward    
    px.set_motor_speed(1, 0)
    px.set_motor_speed(2, speed)
    time.sleep(0.5) 
    #Steering sets to zero
    for angle in range (-35, 5, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)  

def forward_right(px):
    px.set_dir_servo_angle(0)
    for x in range(0,30, 5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1*10) 
    time.sleep(1.25)
    px.stop()
    for x in range(25, -5, -5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)   

def forward_left(px):
    px.set_dir_servo_angle(0)
    for x in range(0,-35, -5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1*10) 
    time.sleep(1.75)
    px.stop()
    for x in range(-35, 5, 5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)   

# ----- Path generation function ------

def generate(start,facing):
        actions = []
        print("••••••••••••••••••••••")
        grid = navigator.load_map("map.txt")  
        goal = navigator.generate_random_goal(grid,start)
        path = navigator.find_shortest_path(grid, start, goal)
        if path:
            directions = navigator.path_to_directions(path)
            relative_directions,facing_rel = navigator.convert_absolute_to_relative(directions,facing)
            actions.extend(relative_directions)
            #final_directions = navigator.simplify_actions(relative_directions)
            print("Path found           :", path)
            print("Absolute directions  :", directions)
            print("Relative Directions  :", relative_directions,facing_rel)
        else:
            print("No path found.")
        return actions

# --- Ultrasonic Functions ---
def read_distance(px):
  safe_distance = 40
  danger_distance = 20
  while True:
            distance = round(px.ultrasonic.read(), 2)
            print("distance: ",distance)
            if distance >= safe_distance:
                print("safe distance")
            elif distance >= danger_distance:
                print("safe but close danger")
            else:
                print("not safe")

# ----------------------------

def update_location_and_facing(current_location, current_action, facing):
    x = int(current_location[0])
    y = int(current_location[1])    

    if current_action == "left":
        if facing == "up":
            facing = "left"
        elif facing == "down":
            facing = "right"
        elif facing == "left":
            facing = "down"
        elif facing == "right":
            facing = "up"    
    elif current_action == "right":
        if facing == "up":
            facing = "right"
        elif facing == "down":
            facing = "left"
        elif facing == "left":
            facing = "up"
        elif facing == "right":
            facing = "down"    
    elif current_action == "reverse":
        if facing == "up":
            facing = "down"
        elif facing == "down":
            facing = "up"
        elif facing == "left":
            facing = "right"
        elif facing == "right":
            facing = "left"
    elif current_action == "forward":
        if facing == "up":
            facing = "up"
            x -= 1
        elif facing == "down":
            facing = "down"
            x += 1
        elif facing == "left":
            facing = "left"
            y -=1
        elif facing == "right":
            facing = "right"
            y += 1

    return (x,y), facing


# --- Auto Mode Functions ---

def auto(px,actions):
    current_location = (3, 3) 
    facing = "up"
    while actions:  # runs while the list is not empty
        distance = round(px.ultrasonic.read(), 2)
        if distance <= 20:  
            print("Obstacle detected")
            print("current location, facing", current_location,facing)
            actions.clear()
            obstacle_location = current_location
            navigator.update_map_cell("map.txt", obstacle_location, 1)
            grid = navigator.load_map("map.txt")
            print(grid)
            actions = generate(current_location,facing)
            time.sleep(2)
            continue            
        current_action = actions.pop(0)  # remove the first item
        print(f"Executing: {current_action}")
        if current_action == "forward":
            move_forward(px)
            current_location, facing = update_location_and_facing(current_location,current_action,facing)
        elif current_action == "reverse":
            move_reverse(px)
            current_location, facing = update_location_and_facing(current_location,current_action,facing)
        elif current_action == "right":
            turn_right(px)
            current_location, facing = update_location_and_facing(current_location,current_action,facing)
        elif current_action == "left":
            turn_left(px)
            current_location, facing = update_location_and_facing(current_location,current_action,facing)
        elif current_action == "stop":
            px.stop()
        elif current_action == "generate":
            actions = generate(current_location,facing)
            actions.append("generate")
        px.stop()
        time.sleep(PAUSE_BETWEEN_ACTIONS)
        print("Location, Facing:",current_action,facing)

    print("All actions completed! \n")
    time.sleep(2)
            
# --- Auto Mode Functions ---
            
def manual(px):
    try:
        print("Entering Manual Mode ... \n")
        current_angle = 0
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('awdopi'):
                if 'i' == key:
                    engine_start(px)
                elif 'o' == key:
                    engine_stop(px)
                elif 'p' == key:
                    engine_reverse(px)
                elif 'a' == key:
                    current_angle = steer_left(px,current_angle)
                elif 'w' == key:
                    current_angle = steer_center(px,current_angle)
                elif 'd' == key:
                    current_angle = steer_right(px,current_angle)

            elif key == readchar.key.CTRL_C:
                break
    except KeyboardInterrupt:
        print("Exiting Manual Mode ... \n")
    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        time.sleep(1)
