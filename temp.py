from robot_hat.utils import reset_mcu
from picarx import Picarx
import time

reset_mcu()
sleep(0.2)

px = Picarx()


def drive( actions: List[str], speed):
    while actions:
        operate = actions.pop[0]
        if operate == 'stop':
            px.stop()  
        else:
            if operate == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(speed)
            elif operate == 'backward':
                px.set_dir_servo_angle(0)
                px.backward(speed)
            elif operate == 'turn left':
                px.set_dir_servo_angle(-30)
                px.forward(speed)
            elif operate == 'turn right':
                px.set_dir_servo_angle(30)
                px.forward(speed)
    px.stop()

def main():
    speed = 25
    actions: List[str] = []

    while True:
        # readkey
        key = readchar.readkey().lower()
        # operation 
        if key in ('wsadfop'):
            # throttle
            if key == 'o':
                if speed <=90:
                    speed += 10           
            elif key == 'p':
                if speed >=10:
                    speed -= 10
                if speed == 0:
                    status = 'stop'
            # direction
            elif key in ('wsad'):
                if speed == 0:
                    speed = 10
                if key == 'w':
                    actions.append('forward')
                elif key == 'a':
                    actions.append('turn left')
                elif key == 's':
                    actions.append('backward')
                elif key == 'd':
                    actions.append('turn right')
            # stop
            elif key == 'f':
                status = 'stop'
        elif key == readchar.key.CTRL_C:
            print("Stopping")
            px.stop()
            break 
    drive(actions,speed)        

if __name__ == "__main__":
    try:
        main()
    except Exception as e:    
        print("error:%s"%e)
    finally:
        px.stop()


