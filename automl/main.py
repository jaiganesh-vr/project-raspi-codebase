from picarx import Picarx  
import driver

px = Picarx()
#actions = ["forward","forward","forward","forward","forward","forward","forward","forward"]
#actions = ["forward","right","forward","right","forward","right","forward",]
actions = ["forward","left","forward","left","forward","left","forward"]
#actions = ["right","forward"]
#actions = ["left", "right", "reverse","forward"]
#actions = ["forward", "reverse", "right", "straight", "left", "straight", "stop"]


if __name__ == "__main__":
    try:
        driver.drive(px,actions)
    except Exception as e:    
        print("error:%s"%e)
    finally:
        px.stop()


