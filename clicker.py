import pydirectinput
import time
import keyboard
import json
import random

# Replace these with your cookie coordinates
# TODO Have these be congfiurable? click cookie to start type of thing
x = 2241 
y = 404

# Config Vars
log_rate = 20
sicko_mode = False
pydirectinput.PAUSE = 0

print("Press F6 to toggle auto-clicking. Press F7 to quit. Press F10 to toggle sicko mode, which could get weird.")
clicking = False

def log_stats():
    now = time.time()
    elapsed = now - start_time
    cps = click_count / elapsed if elapsed > 0 else 0

    print(f"[Stats] Time ran: {elapsed:.1f}s | "
        f"Total Clicks: {click_count} | Avg. CPS: {cps:.2f}")

while True:
    # Toggle clicking
    if keyboard.is_pressed("f6"):
        clicking = not clicking
        print("Clicking:", clicking)

        if clicking:
            # New Session
            with open("sessions.json", "r") as f:
                data = json.load(f)
            session_name=random.choice(data["grandma_names"])

            # TODO Clean this up
            print(f"""                  
Starting new session!
SESSION: {session_name}
--------------------""")
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
        sicko_mode= not sicko_mode

    if clicking:
        # Click and Increment
        pydirectinput.click(x, y)
        click_count += 1
        now = time.time()

        # Log Stats
        if now - last_log_time >= log_rate:
            log_stats()
            last_log_time = now

        if not sicko_mode:
            time.sleep(0.0001)
