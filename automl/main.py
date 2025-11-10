# main.py
import time
from picarx import Picarx   # your hardware file (the big class you pasted)
from driver import Driver

if __name__ == "__main__":
    px = Picarx()
    driver = Driver(px)

    # Example 1: Explore
    driver.set_speed(45)
    driver.set_mode("Explore")
    driver.perform_actions()

    time.sleep(1)

    # Example 2: Race (simulate upshift)
    driver.set_mode("Race")
    # driver.upshift()  # optionally adjust gear in driver before performing actions
    driver.perform_actions()

    # Back to standby
    driver.set_mode("StandBy")
    print("Demo complete.")
