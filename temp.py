from picarx import Picarx
import time


if __name__ == "__main__":
    try:
        # init picarx
        px = Picarx()

        for x in range(-100,0,10):
            px.forward(x)
            print(x)
            time.sleep(10)

    finally:
        px.stop()
        time.sleep(0.2)


