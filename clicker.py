import pydirectinput
import time
import keyboard
import json
import random

# Replace these with your cookie coordinates
x = 2241 
y = 404
pydirectinput.PAUSE = 0

print("Press F6 to toggle auto-clicking. Press F7 to quit.")
clicking = False

def log_stats():
    now = time.time()
    elapsed = now - start_time

    # TODO is this needed
    if elapsed > 3600:  # Cap session at 1 hour cuz im worried about overflow
                click_count = 0
                start_time = time.time()

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

    if clicking:
        # Click and Increment
        pydirectinput.click(x, y)
        click_count += 1
        now = time.time()

        # Log stats every 20 seconds
        if now - last_log_time >= 20:
            elapsed = now - start_time

            log_stats()
            last_log_time = now

        time.sleep(0.0001)
