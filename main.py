#Import modules
import keyboard
import time
import threading


#Configuration

"""Game keybinds(what the application is actually going to monitor)
WASD = Movement
Q = Manual shoot
shift = Intake
J/L = Rotation
K = Shoot at the hub
C = Climb(Only on big dumper as of creation)
V = Special(1678 hopper expansion)
"""
gameKeybinds = {
    "w", "a", "s", "d", "q", "shift", "j", "k", "l", "c", "v"
}

#Recording time(How long the auto is)
autoTime = 20.0

#state of the script(Idle, recording auto, auto in progress)
state = "idle"


#Recording and playback
recording = False
playing = False
stopauto = False

#Variable for storing all keyboard related events(tracking gameKeybinds keys)
keyEvents = []
#Variable for when the recording started for math later on
recordingStart = 0

#Keyboard event, will log if recording, automatically considers caps lock
def controllerlogger(key):
    global keyEvents

    if not recording:
        return

    recordedKey = key.name.lower()

    if recordedKey not in gameKeybinds:
        return

    keyEvents.append({
        "time": time.perf_counter() - recordingStart,
        "key": recordedKey,
        "type": key.event_type
    })
keyboard.hook(controllerlogger)


#Recording starter function
def startAutoLogger(duration=20):
    global recording
    global recordingStart
    global keyEvents

    # Ensure we aren't already recording
    if recording:
        print("Currently recording!")
        return

    # Clear previous recording
    keyEvents.clear()

    print("Auto recording has begun")

    recording = True
    recordingStart = time.perf_counter()

    # Record for the requested duration
    time.sleep(duration)

    recording = False

    print("Finished recording your auto")
    print(f"Recorded {len(keyEvents)} events.")

#Play the auto
def playAuto():
    global playing
    global stopauto

    if playing:
        print("Already playing!")
        return

    if len(keyEvents) == 0:
        print("No auto recorded.")
        return

    playing = True
    stopauto = False

    print("Starting auto")

    previousTime = 0

    for event in keyEvents:

        if stopauto:
            break

        delay = event["time"] - previousTime

        if delay > 0:
            time.sleep(delay)

        if stopauto:
            break

        if event["type"] == "down":
            keyboard.press(event["key"])
        else:
            keyboard.release(event["key"])

        previousTime = event["time"]

    # Safety release
    for key in gameKeybinds:
        keyboard.release(key)

    playing = False

    print("Finished auto")

def stopAuto():
    global stopauto

    stopauto = True

    # Release all keys in case one is held
    for key in gameKeybinds:
        keyboard.release(key)

    print("Auto stopped")
        



keyboard.add_hotkey(
    "\\",
    lambda: threading.Thread(
        target=startAutoLogger,
        daemon=True
    ).start()
)

# Play recording
keyboard.add_hotkey(
    "r",
    lambda: threading.Thread(
        target=playAuto,
        daemon=True
    ).start()
)

# Stop playback
keyboard.add_hotkey(
    "ctrl",
    stopAuto
)

print("MoSimulator AUTO System Ready!")
print("\\ = Record")
print("R = Play")
print("Ctrl = Stop")

keyboard.wait()