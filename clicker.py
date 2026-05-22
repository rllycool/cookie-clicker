import time
import keyboard
import mouse
from mouse import ButtonEvent
import json
import random

import pyautogui
import pydirectinput
pydirectinput.PAUSE = 0

print("Click your cookie to start!")
print("Press F6 to toggle auto-clicking. Press F7 to quit. Press F10 to toggle sicko mode, which could get weird.")

# TODO Configurable Vars
log_rate = 10

# Initialize Vars
clicking = False
sicko_mode = False
start_time = 0
click_count = 0
last_log_time = 0

# Cookie Coords
positions = []
x,y = None,None

def log_stats():
    now = time.time()
    elapsed = now - start_time
    cps = click_count / elapsed if elapsed > 0 else 0

    print(f"[Stats] Time ran: {elapsed:.1f}s | "
        f"Total Clicks: {click_count} | Avg. CPS: {cps:.2f}")
    
def on_click(event):
    global x, y
    if not isinstance(event, ButtonEvent):
        return
    if event.event_type == "down" and x is None:
        # TODO using two different python GUI libs 
        x, y = pyautogui.position()
        print(f"Cookie position set to: {x}, {y}")
        mouse.unhook(on_click)  # stop listening once captured
mouse.hook(on_click)

while True:
    # Toggle clicking
    if keyboard.is_pressed("f6"):
        #TODO lazy error handle
        if x is None:
            print("WARNING - Please set cookie coords before starting a session!")
        
        clicking = not clicking
        print("Clicking:", clicking)

        if clicking:
            # New Session
            with open("sessions.json", "r") as f:
                data = json.load(f)
            session_name=random.choice(data["grandma_names"])

            # TODO Clean this up | xd it got worse
            print(f"Starting new session!\nSESSION: {session_name}\n--------------------")
            start_time = time.time()
            last_log_time = time.time()
        else:
            log_stats()

        click_count = 0
        time.sleep(0.3)  # debounce

    # Quit
    if keyboard.is_pressed("f7"):
        print("Exiting.")
        log_stats()
        break
    
    # Toggle sicko mode 
    if keyboard.is_pressed("f10"): 
        print(f"Speed:{not sicko_mode}")
        sicko_mode= not sicko_mode
        time.sleep(0.3)  # debounce

    # Click and Increment
    if clicking:
        pydirectinput.click(x, y)
        click_count += 1
        now = time.time()

        # Log Stats
        if now - last_log_time >= log_rate:
            log_stats()
            last_log_time = now

        if not sicko_mode:
            time.sleep(0.0001)
