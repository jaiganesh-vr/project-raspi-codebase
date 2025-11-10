# driver.py
import time
from typing import List
from navigator import Navigator

class Driver:
    VALID_MODES = ("StandBy", "Drive", "Race", "Explore")

    def __init__(self, px):
        
        self.px = px
        self.navigator = Navigator(px)
        self.mode = "StandBy"
        self.actions: List[str] = []
        self.speed = 50   # default speed (0-100)
        self.gear = 1     # simple gear: 1 normal, 2 upshift (faster)

    def set_mode(self, mode: str):
        if mode not in self.VALID_MODES:
            raise ValueError(f"Unknown mode {mode}. Valid: {self.VALID_MODES}")
        print(f"[Driver] switching mode -> {mode}")
        self.mode = mode
        self.actions.clear()
        # Build action lists (you can expand sequences as you like)
        if mode == "StandBy":
            self.actions = []
        elif mode == "Drive":
            self.actions = ["Start", "Forward", "Forward", "Right", "Forward", "Stop"]
        elif mode == "Race":
            self.actions = ["Start", "Upshift", "Forward", "Forward", "Right", "Left", "Forward", "Downshift", "Stop"]
        elif mode == "Explore":
            self.actions = ["Start", "Forward", "Left", "Forward", "Right", "Forward", "Reverse", "Stop"]

    def perform_actions(self):
        print("[Driver] Begin action loop. Actions:", self.actions)
        # run until actions list empty or an emergency stops
        while self.actions:
            action = self.actions.pop(0)
            print(f"[Driver] Next action: {action}")
            # Navigator will return whether it completed or if an emergency happened
            completed = self.navigator.manoeuvre(action, speed=self.speed, gear=self.gear)
            # If manoeuvre returned False, we treat it as a stop/abort and break
            if not completed:
                print("[Driver] Manoeuvre requested abort or emergency stop.")
                break
            # brief pause between actions
            time.sleep(0.15)

        # ensure vehicle is stopped at end
        self.px.stop()
        print("[Driver] Action list exhausted. Vehicle stopped.")

    # Convenience API to adjust speed/gear on the fly
    def set_speed(self, speed: int):
        self.speed = max(0, min(100, speed))
        print(f"[Driver] speed set to {self.speed}")

    def upshift(self):
        if self.gear < 3:
            self.gear += 1
        print(f"[Driver] gear -> {self.gear}")

    def downshift(self):
        if self.gear > 1:
            self.gear -= 1
        print(f"[Driver] gear -> {self.gear}")
