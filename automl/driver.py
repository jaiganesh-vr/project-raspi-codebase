from robot_hat.utils import reset_mcu
import navigator
import readchar
import time

# --- Initialization ---
reset_mcu()
time.sleep(2)

start = (3, 3) 
facing = "up"

# --- Constants ---
TURN_SPEED = 10         # Moderate speed for turning
DRIVE_SPEED = 10        # Normal forward driving speed
TURN_TIME_RIGHT = 1.6      # Seconds to complete a 90° turn
TURN_TIME_LEFT = 1.6      # Seconds to complete a 90° turn
TURN_TIME_180 = 3.2     # Seconds to complete a 180° turn
PAUSE_BETWEEN_ACTIONS = 1  # Seconds to pause after each action

def constrain(x, min_val, max_val):
    '''
    Constrains value to be within a range.
    '''
    return max(min_val, min(max_val, x))

# --- Movement Functions ---
def move_forward(px, duration=1.0, speed=DRIVE_SPEED):
    """Move forward for a specified duration."""
    px.set_dir_servo_angle(0)
    px.forward(speed)
    time.sleep(duration)
    px.stop()

def turn_left(px, speed=TURN_SPEED):
    """Turn the car left by ~90 degrees."""
    for angle in range(0, -35, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.110)
    #px.forward(10)
    px.set_motor_speed(1, 0)       # left wheel stopped
    px.set_motor_speed(2, -speed)     
    time.sleep(1.050)    
    px.stop()
    for angle in range(-32, 0, 2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)   

def turn_right(px, speed=TURN_SPEED):
    """Turn the car left by ~90 degrees."""
    for angle in range(0, 35, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.110)
    px.set_motor_speed(1, speed)   # left wheel active
    px.set_motor_speed(2, 0)   
    time.sleep(0.825)
    px.stop()
    for angle in range(30, 0, -2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)   

def reverse(px, speed=TURN_SPEED):
    """Turn the car left by ~90 degrees.""" 
    for angle in range(0, 35, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.110)
    px.set_motor_speed(1, speed)   # left wheel active
    px.set_motor_speed(2, 0)  
    time.sleep(1.350)
    px.stop()
    for angle in range(30, 0, -2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)  

def engine_start(px):
    px.forward(10)

def engine_stop(px):
    px.stop()

def engine_reverse(px):
    px.backward(10)

def steer_left(px):
    current_angle = px.dir_current_angle
    new_angle = current_angle - 5
    final_angle = constrain(new_angle,-30,30)
    for x in range(current_angle, final_angle -2.5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0125)

def steer_right(px):
    current_angle = px.dir_current_angle
    new_angle = current_angle + 5
    final_angle = constrain(new_angle,-30,30)
    for x in range(current_angle, final_angle, 2.5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0125)



def drive(px,actions):
    while actions:  # runs while the list is not empty
        current_action = actions.pop(0)  # remove the first item
        print(f"Executing: {current_action}")
        if current_action == "forward":
            move_forward(px)
        elif current_action == "reverse":
            reverse(px)
        elif current_action == "right":
            turn_right(px)
        elif current_action == "left":
            turn_left(px)
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
                relative_direction,facing = navigator.convert_absolute_to_relative(directions,facing)
                actions.extend(relative_direction)
                print("Directions:", relative_direction,facing)
                actions.append("generate")
            else:
                print("No path found.")
            start = goal
            print(start)

        # Pause between steps
        px.stop()
        time.sleep(PAUSE_BETWEEN_ACTIONS)
    print("All actions completed! \n")

            
def manual(px):
    try:
        print("Entering Manual Mode")
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('adopi'):
                if 'i' == key:
                    engine_start(px)
                elif 'o' == key:
                    engine_stop(px)
                elif 'p' == key:
                    engine_reverse(px)
                elif 'a' == key:
                    steer_left(px)
                elif 'd' == key:
                    steer_right(px)

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
