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

def _step_servo(px, start, end, delay=0.0125):
    """Move servo smoothly from start to end (inclusive)."""
    if start == end:
        px.set_dir_servo_angle(end)
        return
    step = 1 if end > start else -1
    angle = start
    while True:
        px.set_dir_servo_angle(angle)
        time.sleep(delay)
        if angle == end:
            break
        angle += step

# --- Manual Movement Functions ---
def engine_start(px):
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1 * 10)

def engine_stop(px):
    px.stop()

def engine_reverse(px):
    px.set_motor_speed(1, -1 * 10)
    px.set_motor_speed(2, 10)

def steer_left(px, current_angle):
    new_angle = constrain(current_angle - 5, -30, 30)
    _step_servo(px, current_angle, new_angle)
    return new_angle

def steer_center(px, current_angle):
    _step_servo(px, current_angle, 0)
    return 0

def steer_right(px, current_angle):
    new_angle = constrain(current_angle + 5, -30, 30)
    _step_servo(px, current_angle, new_angle)
    return new_angle

# --- Auto Movement Functions ---

def move_forward(px, duration=1.0, speed=DRIVE_SPEED):
    px.set_dir_servo_angle(0)
    px.set_motor_speed(1, speed)
    px.set_motor_speed(2, -1 * speed)
    time.sleep(duration)
    px.stop()

def move_reverse(px, speed=TURN_SPEED):
    for angle in range(0, 35, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    px.set_motor_speed(1, -speed)
    px.set_motor_speed(2, 0)
    time.sleep(1.350)
    px.stop()
    for angle in range(30, -1, -2):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)

def turn_left(px, speed=TURN_SPEED):
    # Steering turns left
    for angle in range(0, -35, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    # Right motor moves forward
    px.set_motor_speed(1, 0)
    px.set_motor_speed(2, -1 * speed)
    time.sleep(0.85)
    px.stop()
    # Steering sets back to zero
    for angle in range(-35, 5, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    # Steering moves right
    for angle in range(0, 40, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    px.set_motor_speed(1, -1 * speed)
    px.set_motor_speed(2, 0)
    time.sleep(0.5)
    for angle in range(30, -5, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)

def turn_right(px, speed=TURN_SPEED):
    # Steering turns right
    for angle in range(0, 35, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    # Left motor move forward
    px.set_motor_speed(1, speed)
    px.set_motor_speed(2, 0)
    time.sleep(0.5)
    px.stop()
    # Steering sets back to zero
    for angle in range(30, -5, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    # Steering turns left
    for angle in range(0, -35, -5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)
    # Right motor moves backward    
    px.set_motor_speed(1, 0)
    px.set_motor_speed(2, speed)
    time.sleep(0.5)
    # Steering sets to zero
    for angle in range(-35, 5, 5):
        px.set_dir_servo_angle(angle)
        time.sleep(0.0525)

def forward_right(px):
    px.set_dir_servo_angle(0)
    for x in range(0, 30, 5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1 * 10)
    time.sleep(1.25)
    px.stop()
    for x in range(25, -5, -5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)

def forward_left(px):
    px.set_dir_servo_angle(0)
    for x in range(0, -35, -5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)
    px.set_motor_speed(1, 10)
    px.set_motor_speed(2, -1 * 10)
    time.sleep(1.75)
    px.stop()
    for x in range(-35, 5, 5):
        px.set_dir_servo_angle(x)
        time.sleep(0.0525)

def generate(start, facing):
    actions = []
    print("••••••••••••••••••••••")
    grid = navigator.load_map("map.txt")
    goal = navigator.generate_random_goal(grid, start)
    path = navigator.find_shortest_path(grid, start, goal)
    if path:
        directions = navigator.path_to_directions(path)
        relative_directions, facing_rel = navigator.convert_absolute_to_relative(directions, facing)
        actions.extend(relative_directions)
        print("Path found           :", path)
        print("Absolute directions  :", directions)
        print("Relative Directions  :", relative_directions, facing)
    else:
        print("No path found.")
    return actions, facing_rel

# --- Ultrasonic Functions ---
def read_distance(px):
    safe_distance = 40
    danger_distance = 20
    while True:
        distance = round(px.ultrasonic.read(), 2)
        print("distance: ", distance)
        if distance >= safe_distance:
            print("safe distance")
        elif distance >= danger_distance:
            print("safe but close danger")
        else:
            print("not safe")

# --- Camera Mode Functions ---

def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))

def stare_at(px):
    Vilib.camera_start()
    Vilib.display()
    Vilib.face_detect_switch(True)
    x_angle = 0
    y_angle = 0
    while True:
        if Vilib.detect_obj_parameter['human_n'] != 0:
            coordinate_x = Vilib.detect_obj_parameter['human_x']
            coordinate_y = Vilib.detect_obj_parameter['human_y']

            # change the pan-tilt angle for track the object
            x_angle += (coordinate_x * 10 / 640) - 5
            x_angle = clamp_number(x_angle, -35, 35)
            px.set_cam_pan_angle(x_angle)

            # use same sign convention for tilt as pan (adjust if your camera uses inverted axis)
            y_angle += (coordinate_y * 10 / 480) - 5
            y_angle = clamp_number(y_angle, -35, 35)
            px.set_cam_tilt_angle(y_angle)

            time.sleep(0.05)
        else:
            time.sleep(0.05)

# ---------------------------

def update_location(current_location, previous_action, current_action):
    # Keep this function if you need the old rule-based location update.
    x, y = int(current_location[0]), int(current_location[1])

    if previous_action.strip() == "":
        previous_action = "up"

    if previous_action == "up":
        if current_action == "forward":
            y += 1
        elif current_action == "back":
            y -= 1
        elif current_action == "left":
            x -= 1
        elif current_action == "right":
            x += 1

    elif previous_action == "down":
        if current_action == "forward":
            y -= 1
        elif current_action == "back":
            y += 1
        elif current_action == "left":
            x += 1
        elif current_action == "right":
            x -= 1

    elif previous_action == "left":
        if current_action == "forward":
            x -= 1
        elif current_action == "back":
            x += 1
        elif current_action == "left":
            y -= 1
        elif current_action == "right":
            y += 1

    elif previous_action == "right":
        if current_action == "forward":
            x += 1
        elif current_action == "back":
            x -= 1
        elif current_action == "left":
            y += 1
        elif current_action == "right":
            y -= 1

    return (x, y)

def update_location_and_facing(current_location, previous_facing, action):
    """
    Returns: (x, y), new_facing
    - accepts 'forward', 'back' (or 'reverse'), 'left', 'right'
    - turning actions update facing but don't change position
    """
    # ensure coordinates are ints
    x = int(current_location[0])
    y = int(current_location[1])

    # Default facing if none given
    if previous_facing is None or str(previous_facing).strip() == "":
        previous_facing = "up"

    # All possible facings in order
    facings = ["up", "right", "down", "left"]

    # Helper to rotate left/right
    def turn(facing, direction):
        idx = facings.index(facing)
        if direction == "left":
            return facings[(idx - 1) % 4]
        elif direction == "right":
            return facings[(idx + 1) % 4]
        return facing  # no turn

    # normalize synonyms
    normalized_action = "back" if action == "reverse" else action

    # If action is a turn, update facing first (no move)
    if normalized_action in ("left", "right"):
        new_facing = turn(previous_facing, normalized_action)
        return (x, y), new_facing

    # move according to facing
    new_facing = previous_facing

    if previous_facing == "up":
        if normalized_action == "forward":
            y += 1
        elif normalized_action == "back":
            y -= 1

    elif previous_facing == "down":
        if normalized_action == "forward":
            y -= 1
        elif normalized_action == "back":
            y += 1

    elif previous_facing == "left":
        if normalized_action == "forward":
            x -= 1
        elif normalized_action == "back":
            x += 1

    elif previous_facing == "right":
        if normalized_action == "forward":
            x += 1
        elif normalized_action == "back":
            x -= 1

    return (x, y), new_facing


# --- Auto Mode Functions ---

def auto(px, actions):
    current_location = (3, 3)
    facing = "up"
    while actions:  # runs while the list is not empty
        distance = round(px.ultrasonic.read(), 2)
        if distance <= 20:
            print("Obstacle detected")
            print("Current Location", current_location)
            actions.clear()
            px.stop()
            break

        current_action = actions.pop(0)  # remove the first item
        print(f"Executing: {current_action}")

        # map 'reverse' to 'back' inside update function, and always unpack both outputs
        if current_action == "forward":
            move_forward(px)
            current_location, facing = update_location_and_facing(current_location, facing, current_action)
            print(current_location, facing)

        elif current_action in ("back", "reverse"):
            # if 'reverse' do the robot reverse motion but treat as 'back' for location
            move_reverse(px)
            current_location, facing = update_location_and_facing(current_location, facing, "back")
            print(current_location, facing)

        elif current_action == "right":
            turn_right(px)
            current_location, facing = update_location_and_facing(current_location, facing, current_action)
            print(current_location, facing)

        elif current_action == "left":
            turn_left(px)
            current_location, facing = update_location_and_facing(current_location, facing, current_action)
            print(current_location, facing)

        elif current_action == "stop":
            px.stop()

        elif current_action == "generate":
            actions, facing = generate(current_location, facing)

        px.stop()
        time.sleep(PAUSE_BETWEEN_ACTIONS)

    print("All actions completed! \n")
    time.sleep(2)

# --- Manual Mode ---

def manual(px):
    try:
        print("Entering Manual Mode ... \n")
        current_angle = 0
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in ('awdopi'):
                if 'i' == key:
                    engine_start(px)
                elif 'o' == key:
                    engine_stop(px)
                elif 'p' == key:
                    engine_reverse(px)
                elif 'a' == key:
                    current_angle = steer_left(px, current_angle)
                elif 'w' == key:
                    current_angle = steer_center(px, current_angle)
                elif 'd' == key:
                    current_angle = steer_right(px, current_angle)

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
