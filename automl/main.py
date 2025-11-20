from robot_hat.utils import reset_mcu
from picarx import Picarx  
import threading
import readchar
import helper
import driver
import time

# --- Initialization ---
reset_mcu()
time.sleep(2)

manual = '''
Select one of the following mode for Picar X :)
    a: Auto
    m: Manual
    e: Explore
    r: Race
    ctrl+c: Quit
'''
def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    voltage = helper.get_battery_voltage()
    level = helper.map_voltage_to_percent(voltage)
    print(manual)
    print(f"Battery Voltage: {voltage:.2f} V | Level: {level:.1f}% \n")

# --- Camera Mode Functions ---

def clamp_number(num,a,b):
  return max(min(num, max(a, b)), min(a, b))

def stare_at(px):
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

            time.sleep(0.05)

        else :
            pass
            time.sleep(0.05)


if __name__ == "__main__":

    try:
        px = Picarx()
        while True:
            show_info()
            key = readchar.readkey()
            key = key.lower()
            if key in('amer'):
                if 'a' == key:
                    actions = ["generate"]
                    t1 = threading.Thread(target=driver.auto(px,actions))
                    t2 = threading.Thread(stare_at(px))
                    t1.start()
                    t2.start()
                elif 'm' == key:
                    driver.manual(px)
                elif 'e' == key:
                    driver.explore()
                elif 'r' == key:
                    driver.race()

            elif key == readchar.key.CTRL_C:
                break
    except KeyboardInterrupt:
        print("Bye! 👋 \n")

    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        time.sleep(1)