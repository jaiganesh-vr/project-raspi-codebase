import time
from picarx import Picarx 
from driver import Driver

if __name__ == "__main__":
    px = Picarx()
    
    px.forward(30)
    time.sleep(0.5)