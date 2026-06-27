import keyboard
from autosystem import autoRecorder

AUTO = autoRecorder()

keyboard.add_hotkey("\\", AUTO.startRecordingThread)
keyboard.add_hotkey("]", AUTO.playThread)
keyboard.add_hotkey("ctrl", AUTO.stop)

print("MoSimulator AUTO System Ready!")

keyboard.wait()