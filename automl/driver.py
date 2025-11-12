from robot_hat.utils import reset_mcu
import navigator
import readchar
import time

# --- Initialization ---
reset_mcu()
time.sleep(2)

# --- Constants ---
TURN_SPEED = 10         # Moderate speed for turning
DRIVE_SPEED = 10        # Normal forward driving speed
TURN_TIME_RIGHT = 1.6      # Seconds to complete a 90° turn
TURN_TIME_LEFT = 1.6      # Seconds to complete a 90° turn
TURN_TIME_180 = 3.2     # Seconds to complete a 180° turn
PAUSE_BETWEEN_ACTIONS = 1  # Seconds to pause after each action

# --- Helper Functions ---
def constrain(x, min_val, max_val):
    '''
    Constrains value to be within a range.
    '''
    return max(min_val, min(max_val, x))

# --- Manual Movement Functions ---
def engine_start(px):
    px.set_dir_servo_angle(0)
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1*10) 

def engine_stop(px):
    px.stop()

def engine_reverse(px):
    px.set_dir_servo_angle(0)
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
    for angle in range(30, 10, -5):
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
    for angle in range(30, 5, -5):
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
    for x in range(25, 5, -5):
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

# --- Drive Mode Functions ---

def auto(px,actions):
    start = (2, 2) 
    facing = "up"
    while actions:  # runs while the list is not empty
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
        elif current_action == "generate":
            grid = navigator.load_map("map.txt")  
            print(start)    
            goal = navigator.generate_random_goal(grid,start)
            path = navigator.find_shortest_path(grid, start, goal)
            if path:
                print("Path found:", path)
                directions = navigator.path_to_directions(path)
                print(directions)
                relative_directions,facing = navigator.convert_absolute_to_relative(directions,facing)
                final_directions = navigator.simplify_actions(relative_directions)
                actions.extend(final_directions)
                print("Directions:", final_directions,facing)
                actions.append("generate")
            else:
                print("No path found.")
            start = goal
            print(start)

        # Pause between steps
        px.stop()
        time.sleep(PAUSE_BETWEEN_ACTIONS)
    print("All actions completed! \n")
    time.sleep(2)
            
def manual(px):
    try:
        print("Entering Manual Mode \n")
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
        print("Exiting Manual Mode.\n")
    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        time.sleep(1)
