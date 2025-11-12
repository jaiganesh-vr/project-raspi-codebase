from robot_hat.utils import reset_mcu
from picarx import Picarx  
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


if __name__ == "__main__":

    try:
        px = Picarx()
        while True:
            show_info()
            key = readchar.readkey()
            key = key.lower()
            if key in('amer'):
                if 'a' == key:
                    actions = ["forward_left"]
                    driver.auto(px,actions)
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