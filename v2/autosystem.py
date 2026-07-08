import keyboard
import threading
import time
import json
import os

DEFAULT_KEYBIND_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keybinds_config.json")

class autoRecorder:
    def __init__(self, gameKeybinds=None, hotkeys=None):
        # Configuration
        self.gameKeybinds = set(gameKeybinds) if gameKeybinds else {
            "w", "a", "s", "d",
            "q",
            "shift",
            "j", "k", "l",
            "c", "v"
        }

        self.hotkeys = dict(hotkeys) if hotkeys else {
            "record": "\\",
            "play": "]",
            "stop": "ctrl"
        }

        self.autoTime = 20.0

        # State
        self.state = "Idle"

        self.recording = False
        self.playing = False
        self.stopAuto = False

        # Recorded data
        self.keyEvents = []
        self.recordingStart = 0

        # Hotkey handlers (for removal/re-registration)
        self._hotkeyHandlers = []

        # Setup keyboard input logger
        keyboard.hook(self.controllerLogger)

        # Register initial hotkeys
        self._registerHotkeys()

    def _registerHotkeys(self):
        for handler in self._hotkeyHandlers:
            keyboard.remove_hotkey(handler)
        self._hotkeyHandlers.clear()
        self._hotkeyHandlers.append(
            keyboard.add_hotkey(self.hotkeys["record"], self.startRecordingThread)
        )
        self._hotkeyHandlers.append(
            keyboard.add_hotkey(self.hotkeys["play"], self.playThread)
        )
        self._hotkeyHandlers.append(
            keyboard.add_hotkey(self.hotkeys["stop"], self.stop)
        )

    def setGameKeybinds(self, keybinds):
        self.gameKeybinds = set(keybinds)

    def getGameKeybinds(self):
        return sorted(self.gameKeybinds)

    def setHotkeys(self, hotkeys):
        old = dict(self.hotkeys)
        self.hotkeys.update(hotkeys)
        if self.hotkeys != old:
            self._registerHotkeys()

    def getHotkeys(self):
        return dict(self.hotkeys)

    def saveKeybindConfig(self, filename=None):
        if filename is None:
            filename = DEFAULT_KEYBIND_CONFIG_PATH
        data = {
            "gameKeybinds": sorted(self.gameKeybinds),
            "hotkeys": self.hotkeys
        }
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Saved keybind config to {filename}")
        except Exception as e:
            print(f"Failed to save keybind config: {e}")

    def loadKeybindConfig(self, filename=None):
        if filename is None:
            filename = DEFAULT_KEYBIND_CONFIG_PATH
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            if "gameKeybinds" in data:
                self.gameKeybinds = set(data["gameKeybinds"])
            if "hotkeys" in data:
                self.hotkeys.update(data["hotkeys"])
                self._registerHotkeys()
            print(f"Loaded keybind config from {filename}")
        except FileNotFoundError:
            print(f"No keybind config found at {filename}, using defaults")
        except Exception as e:
            print(f"Failed to load keybind config: {e}")


    #Recording systems
    #Logger
    def controllerLogger(self, key):

        if not self.recording:
            return

        recordedKey = key.name.lower()

        if recordedKey not in self.gameKeybinds:
            return

        self.keyEvents.append({
            "time": time.perf_counter() - self.recordingStart,
            "key": recordedKey,
            "type": key.event_type
        })
    
    #Recorder starter
    def startRecording(self, duration=None):

        if duration is None:
            duration = self.autoTime
        if self.playing:
            print("Cannot record while playing.")
            return

        if self.recording:
            print("Already recording.")
            return

        self.keyEvents.clear()

        self.recording = True
        self.state = "Recording"

        time.sleep(1)
        keyboard.press_and_release("r")

        self.recordingStart = time.perf_counter()

        print("Recording started.")

        time.sleep(duration)

        self.recording = False
        self.state = "Idle"

        print(f"Finished recording ({len(self.keyEvents)} events).")

    #Recording starter
    def startRecordingThread(self):
        threading.Thread(
            target=self.startRecording,
            daemon=True
        ).start()


    # playback systems
    def play(self):

        if self.playing:
            return
        if self.recording:
            print("Cannot play while recording.")
            return

        if len(self.keyEvents) == 0:
            print("No auto recorded.")
            return

        self.playing = True
        self.stopAuto = False
        self.state = "Playing"

        time.sleep(1)
        keyboard.press_and_release("r")

        print("Playing auto...")

        previousTime = 0

        for event in self.keyEvents:

            if self.stopAuto:
                break

            delay = event["time"] - previousTime

            if delay > 0:
                time.sleep(delay)

            if self.stopAuto:
                break

            if event["type"] == "down":
                keyboard.press(event["key"])
            else:
                keyboard.release(event["key"])

            previousTime = event["time"]

        # Release every key just in case
        for key in self.gameKeybinds:
            keyboard.release(key)

        self.playing = False
        self.state = "Idle"

        print("Finished auto.")

    def playThread(self):
        threading.Thread(
            target=self.play,
            daemon=True
        ).start()

    def stop(self):

        self.stopAuto = True

        for key in self.gameKeybinds:
            keyboard.release(key)

        self.playing = False
        self.state = "Idle"

        print("Playback stopped.")
    
    def clearAuto(self):
        self.keyEvents.clear()

    def saveAuto(self, filename):
        data = {
            "version": 1,
            "events": self.keyEvents
        }

        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4) 
            print(f"Saved auto to {filename}")

        except Exception as e:
            print(e)
    
    def loadAuto(self, filename):
        try:

            with open(filename, "r") as file:
                data = json.load(file)

            self.keyEvents = data.get("events", [])

            print(f"Loaded auto from {filename}")

        except Exception as e:
            print(e)
    def getAutoNames(self):

        import os

        if not os.path.exists("autos"):
            return []

        return sorted(
            file[:-5]
            for file in os.listdir("autos")
            if file.endswith(".json")
        )

    #Helper functions(used in ui and stuff)
    def getState(self):
        return self.state

    def getEventCount(self):
        return len(self.keyEvents)

    def getEvents(self):
        return self.keyEvents