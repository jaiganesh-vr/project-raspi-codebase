from picarx import Picarx  
import driver

px = Picarx()

actions = ["left","right","reverse"]

if __name__ == "__main__":
    try:
        driver.drive(px,actions)
    except Exception as e:    
        print("error:%s"%e)
    finally:
        px.stop()


