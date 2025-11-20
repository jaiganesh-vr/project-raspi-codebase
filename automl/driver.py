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
    time.sleep(0.65)    
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

# --- Auto Mode Functions ---
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
# --- Camera Mode Functions ---

def clamp_number(num,a,b):
  return max(min(num, max(a, b)), min(a, b))

def stare_at():
    Vilib.camera_start()
    Vilib.display()
    Vilib.face_detect_switch(True)
    x_angle =0
    y_angle =0
    while True:
        if Vilib.detect_obj_parameter['human_n']!=0:
            coordinate_x = Vilib.detect_obj_parameter['human_x']
            coordinate_y = Vilib.detect_obj_parameter['human_y']
            
            # change the pan-tilt angle for track the object
            x_angle +=(coordinate_x*10/640)-5
            x_angle = clamp_number(x_angle,-35,35)
            px.set_cam_pan_angle(x_angle)

            y_angle -=(coordinate_y*10/480)-5
            y_angle = clamp_number(y_angle,-35,35)
            px.set_cam_tilt_angle(y_angle)

            sleep(0.05)

        else :
            pass
            sleep(0.05)


# --- Auto Mode Functions ---

def auto(px,actions):
    start = (3, 3) 
    facing = "up"
    stare_at()
    while actions:  # runs while the list is not empty
        distance = round(px.ultrasonic.read(), 2)
        if distance <= 20:
            print("Obstacle detected")
            actions.clear()
            px.stop()
            break
        current_action = actions.pop(0)  # remove the first item
        print(f"Executing: {current_action}")
        if current_action == "forward":
            move_forward(px)
        elif current_action == "reverse":
            move_reverse(px)
        elif current_action == "right":
            turn_right(px)
        elif current_action == "left":
            turn_left(px)
        elif current_action == "forward_left":
            forward_left(px)
        elif current_action == "forward_right":
            forward_right(px)
        elif current_action == "stop":
            px.stop()
        elif current_action == "read":
            read_distance(px)
        elif current_action == "generate":
            print("••••••••••••••••••••••")
            grid = navigator.load_map("map.txt")  
            goal = navigator.generate_random_goal(grid,start)
            path = navigator.find_shortest_path(grid, start, goal)
            if path:
                directions = navigator.path_to_directions(path)
                relative_directions,facing = navigator.convert_absolute_to_relative(directions,facing)
                final_directions = navigator.simplify_actions(relative_directions)
                actions.extend(final_directions)
                actions.append("generate")
                print("Path found           :", path)
                print("Absolute directions  :", directions)
                print("Relative Directions  :", final_directions,facing)
            else:
                print("No path found.")
            start = goal

        px.stop()
        time.sleep(PAUSE_BETWEEN_ACTIONS)

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
