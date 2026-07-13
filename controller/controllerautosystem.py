import keyboard
import threading
import time
import json
import os
from inputs import get_gamepad
import vgamepad as vg

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gamepad_config.json")

class controllerAuto:
    def __init__(self, hotkeys=None):
        # init an xbox 360 controller
        self.v_gamepad = vg.VX360Gamepad()

        # auto control hotkeys
        self.hotkeys = dict(hotkeys) if hotkeys else {
            "record": "\\",
            "play": "]",
            "stop": "ctrl"
        }

        self.autoTime = 20.0  # auto duration

        # auto recorder state(used for gui application)
        self.state = "Idle"
        self.recording = False
        self.playing = False
        self.stopAuto = False
        self.interceptor_running = True

        # joystick axis caching(basically hold the data in variable)
        self.axis_state = {
            "LX": 0, "LY": 0,
            "RX": 0, "RY": 0
        }

        # recorded data
        self.AutoEvents = []
        self.recordingStart = 0

        # hotkey shortcut handler tracking
        self._hotkeyHandlers = []
        self._registerHotkeys()

        # start gamepad interception and larping loop in a seperate thread
        self.interceptor_thread = threading.Thread(target=self._interceptor_loop, daemon=True)
        self.interceptor_thread.start()
        pass
    def _registerHotkeys(self):
        for handler in self._hotkeyHandlers:
            keyboard.remove_hotkey(handler)
        self._hotkeyHandlers.clear()

        self._hotkeyHandlers.append(keyboard.add_hotkey(self.hotkeys["record"], self.startRecordingThread))
        self._hotkeyHandlers.append(keyboard.add_hotkey(self.hotkeys["play"], self.playThread))
        self._hotkeyHandlers.append(keyboard.add_hotkey(self.hotkeys["stop"], self.stop))
    # value clamper, used for clamping joystick values
    def clamp(self, val):
        return max(-32768, min(val, 32767))
    # in event of custom sensitivity
    def scale_axis(self, val):
        return self.clamp(int(val * 1))
    
    #yoinked from controllerSystem
    # this basically js takes values from ur controller and plays them on the virtual controller, HidHide needed
    def _apply_event(self, code, state):
        # left joystick
        if code == 'ABS_X':
            self.axis_state["LX"] = self.scale_axis(state)
            self.v_gamepad.left_joystick(x_value=self.axis_state["LX"], y_value=self.axis_state["LY"])
        elif code == 'ABS_Y':
            self.axis_state["LY"] = self.scale_axis(state) 
            self.v_gamepad.left_joystick(x_value=self.axis_state["LX"], y_value=self.axis_state["LY"])

        # right joystick
        elif code == 'ABS_RX':
            self.axis_state["RX"] = self.scale_axis(state)
            self.v_gamepad.right_joystick(x_value=self.axis_state["RX"], y_value=self.axis_state["RY"])
        elif code == 'ABS_RY':
            self.axis_state["RY"] = self.scale_axis(state)
            self.v_gamepad.right_joystick(x_value=self.axis_state["RX"], y_value=self.axis_state["RY"])

        # triggers
        elif code == 'ABS_Z': 
            self.v_gamepad.left_trigger(value=state)
        elif code == 'ABS_RZ': 
            self.v_gamepad.right_trigger(value=state)

        # other buttons
        elif code == 'BTN_SOUTH': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif code == 'BTN_EAST':  
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        elif code == 'BTN_NORTH': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        elif code == 'BTN_WEST':  
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

        # bumper buttons or whatever you wanna call them or thumbstick presses
        elif code == 'BTN_TL': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        elif code == 'BTN_TR': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        elif code == 'BTN_THUMBL': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        elif code == 'BTN_THUMBR': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

        # start and select
        elif code == 'BTN_START': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        elif code == 'BTN_SELECT': 
            self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK) if state else self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

        # d pad x
        elif code == 'ABS_HAT0X': 
            if state == -1:
                self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            elif state == 1:
                self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            else:
                self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
                self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        # d pad y
        elif code == 'ABS_HAT0Y': 
            if state == -1:
                self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            elif state == 1:
                self.v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            else:
                self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
                self.v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    def _interceptor_loop(self):
        # background gamepad interceptor loop, js runs in the background
        print("Gamepad Interception active.")
        while self.interceptor_running:
            try:
                events = get_gamepad()
                for event in events:
                    # if no auto, js keep updating it
                    if not self.playing:
                        self._apply_event(event.code, event.state)
                        self.v_gamepad.update()

                    # log if recording
                    if self.recording:
                        self.AutoEvents.append({
                            "time": time.perf_counter() - self.recordingStart,
                            "code": event.code,
                            "state": event.state
                        })
            except Exception as e:
                print(f"Gamepad disconnected or error: {e}")
                break

    # recording stuff
    def startRecording(self, duration=None):
        if duration is None:
            duration = self.autoTime
        if self.playing:
            print("Cannot record while playing.")
            return
        if self.recording:
            print("Already recording.")
            return

        self.AutoEvents.clear()
        self.recording = True
        self.state = "Recording"
        #reset game
        time.sleep(1)
        keyboard.press_and_release("r")
        
        print("Recording started. Move your gamepad sticks/buttons now...")
        self.recordingStart = time.perf_counter()

        time.sleep(duration)

        self.recording = False
        self.state = "Idle"
        print(f"Finished recording ({len(self.AutoEvents)} controller events).")

    def startRecordingThread(self):
        threading.Thread(target=self.startRecording, daemon=True).start()

    # epic playback so that auto goes autonomous
    def play(self):
        if self.playing:
            return
        if self.recording:
            print("Cannot play while recording.")
            return
        if len(self.AutoEvents) == 0:
            print("No controller Auto recorded yet.")
            return

        self.playing = True
        self.stopAuto = False
        self.state = "Playing"
        # reset game
        time.sleep(1)
        keyboard.press_and_release("r")

        print("Playing gamepad Auto...")
        previousTime = 0

        for event in self.AutoEvents:
            if self.stopAuto:
                break

            delay = event["time"] - previousTime
            if delay > 0:
                time.sleep(delay)

            if self.stopAuto:
                break

            # send data to fake controller to update
            self._apply_event(event["code"], event["state"])
            self.v_gamepad.update()

            previousTime = event["time"]
        # ensure gamepad inputs are cleaned up after auto
        self.v_gamepad.reset()
        self.v_gamepad.update()
        self.axis_state = {"LX": 0, "LY": 0, "RX": 0, "RY": 0}

        self.playing = False
        self.state = "Idle"
        print("Finished Auto playback.")

    def playThread(self):
        threading.Thread(target=self.play, daemon=True).start()

    def stop(self):
        self.stopAuto = True
        self.recording = False
        self.playing = False
        self.state = "Idle"
        print("Auto actions stopped.")
        #reset all inputs to prevent held buttons
        self.v_gamepad.reset()
        self.v_gamepad.update()
        self.axis_state = {"LX": 0, "LY": 0, "RX": 0, "RY": 0}

    # jSON saving and loading
    def saveAuto(self, filename):
        data = {"version": 1, "events": self.AutoEvents}
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Saved Auto to {filename}")
        except Exception as e:
            print(f"Save failed: {e}")

    def loadAuto(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            self.AutoEvents = data.get("events", [])
            print(f"Loaded Auto from {filename} ({len(self.AutoEvents)} events)")
        except Exception as e:
            print(f"Load failed: {e}")

    def saveConfig(self, filename=DEFAULT_CONFIG_PATH):
        try:
            with open(filename, "w") as f:
                json.dump({"hotkeys": self.hotkeys}, f, indent=4)
        except Exception as e:
            print(f"Failed to save hotkeys: {e}")

    def loadConfig(self, filename=DEFAULT_CONFIG_PATH):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            if "hotkeys" in data:
                self.hotkeys.update(data["hotkeys"])
                self._registerHotkeys()
        except FileNotFoundError:
            pass

    # --- UI Helpers ---
    def getState(self): return self.state
    def getEventCount(self): return len(self.AutoEvents)
    def getHotkeys(self): return self.hotkeys
    def setHotkeys(self, dic):
        self.hotkeys.update(dic)
        self._registerHotkeys()
    def getGameKeybinds(self): return self.game_keybinds
    def setGameKeybinds(self, lst): self.game_keybinds = lst
    def getState(self): return self.state
    def getEventCount(self): 
        return len(self.AutoEvents)

    def saveKeybindConfig(self):
        try:
            with open("keybinds_config.json", "w") as f:
                json.dump({"hotkeys": self.hotkeys, "game_keys": self.game_keybinds}, f, indent=4)
        except Exception as e:
            print(f"Failed configuration dump: {e}")

    def loadKeybindConfig(self):
        if os.path.exists("keybinds_config.json"):
            try:
                with open("keybinds_config.json", "r") as f:
                    data = json.load(f)
                if "hotkeys" in data: self.hotkeys.update(data["hotkeys"])
                if "game_keys" in data: self.game_keybinds = data["game_keys"]
                self._registerHotkeys()
            except Exception as e:
                print(f"Failed configuration recovery: {e}")


if __name__ == "__main__":
    # Create instance; it will start listening to the controller in the background automatically
    recorder = controllerAuto()
    
    print("Commands:")
    print(" Press '\\' to record gamepad inputs for 20 seconds.")
    print(" Press ']' to play back your recorded gamepad Auto.")
    print(" Press 'Ctrl' to interrupt recording or playback.")
    print("\nKeep this console window open to test. Press Ctrl+C inside terminal to exit application.")
    
    # Keep the main script alive so background threads can run
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        recorder.interceptor_running = False
        print("\nExiting cleaner.")