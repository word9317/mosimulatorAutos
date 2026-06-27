import keyboard
import threading
import time

class autoRecorder:
    def __init__(self):
        # Configuration
        self.gameKeybinds = {
            "w", "a", "s", "d",
            "q",
            "shift",
            "j", "k", "l",
            "c", "v"
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

        # Setup keyboard input logger
        keyboard.hook(self.controllerLogger)


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


    #Helper functions(used in ui and stuff)
    def getState(self):
        return self.state

    def getEventCount(self):
        return len(self.keyEvents)

    def getEvents(self):
        return self.keyEvents