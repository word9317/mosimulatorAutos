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
    #Get the events variable(namespaces = stinky)
    global keyEvents
    #Only log if we are recording
    if not recording:
        return
    #get lowercase version of the key
    recordedKey = key.name.lower()
    #Prevent processing of key's that are not used in mosimulator
    if recordedKey not in gameKeybinds:
        return
    
    keyEvents.append({"time": time.perf_counter() - recordingStart, "key": key, "type": key.event_type})

keyboard.hook(controllerlogger)


#Recording starter function
def startAutoLogger(duration=20):
    #namespaces are stinky so i global the earth
    global recording
    global recordingStartglobal
    global keyEvents
    #Ensure the program is not recording events before recording
    if recording:
        print("Currently recording, cannot start another one!")
        return
    print("Auto recording has begun")
    #Fetch current time
    recordingStart = time.perf_counter()
    recording = True
    #sleepy time, Threading takes care of the logger so the program doesnt go kaboom
    time.sleep(duration)

    recording = False
    print("Finished recording your auto")
    print(str(keyEvents))

keyboard.add_hotkey("\\", lambda: threading.Thread(target=startAutoLogger, daemon=True).start())

keyboard.wait()