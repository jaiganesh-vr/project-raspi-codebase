from picarx import Picarx  
import readchar
import driver
import time

manual = '''
Select one of the following mode for Picar X :)
    d: Drive
    m: Manual
    e: Explore
    r: Race
    ctrl+c: Quit
'''
def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)

actions = ["left","right","reverse","forward"]


if __name__ == "__main__":
   
    try:
        px = Picarx()
        show_info()
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('dmer'):
                if 'd' == key:
                    driver.drive(px,actions)
                    break
                elif 'm' == key:
                    driver.manual()
                elif 'e' == key:
                    px.set_dir_servo_angle(-35)
                    px.forward(80)
                elif 'r' == key:
                    px.set_dir_servo_angle(35)
                    px.forward(80)

            elif key == readchar.key.CTRL_C:
                print("\n Quit")
                break
    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        sleep(.2)