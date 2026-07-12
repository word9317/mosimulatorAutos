import threading
from inputs import get_gamepad
import vgamepad as vg

#larp of a controller
v_gamepad = vg.VX360Gamepad()

# tracking joysticks
state = {
    "LX": 0, "LY": 0,
    "RX": 0, "RY": 0
}

def clamp(val):
    return max(-32768, min(val, 32767))

def scale_axis(val):
    return clamp(int(val * 1))

print("Interception active. Press Ctrl+C in the console to stop.")

try:
    while True:
        events = get_gamepad()
        for event in events:
            
            # left joystick
            if event.code == 'ABS_X':
                state["LX"] = scale_axis(event.state)
                v_gamepad.left_joystick(x_value=state["LX"], y_value=state["LY"])
            elif event.code == 'ABS_Y':
                state["LY"] = scale_axis(event.state) 
                v_gamepad.left_joystick(x_value=state["LX"], y_value=state["LY"])


            # --- RIGHT JOYSTICK ---
            elif event.code == 'ABS_RX':
                state["RX"] = scale_axis(event.state)
                v_gamepad.right_joystick(x_value=state["RX"], y_value=state["RY"])
            elif event.code == 'ABS_RY':
                state["RY"] = scale_axis(event.state)
                v_gamepad.right_joystick(x_value=state["RX"], y_value=state["RY"])


            # --- ANALOG TRIGGERS (0 to 255) ---
            elif event.code == 'ABS_Z': # Left Trigger
                v_gamepad.left_trigger(value=event.state)
            elif event.code == 'ABS_RZ': # Right Trigger
                v_gamepad.right_trigger(value=event.state)

            # --- FACE BUTTONS ---
            elif event.code == 'BTN_SOUTH': # A Button
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            elif event.code == 'BTN_EAST':  # B Button
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            elif event.code == 'BTN_NORTH': # X Button
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            elif event.code == 'BTN_WEST':  # Y Button
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

            # --- BUMPERS & STICK CLICKS ---
            elif event.code == 'BTN_TL': # Left Bumper (LB)
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            elif event.code == 'BTN_TR': # Right Bumper (RB)
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            elif event.code == 'BTN_THUMBL': # Left Stick Click
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
            elif event.code == 'BTN_THUMBR': # Right Stick Click
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

            # --- SYSTEM BUTTONS ---
            elif event.code == 'BTN_START': # Menu / Start
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            elif event.code == 'BTN_SELECT': # View / Back
                v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK) if event.state else v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

            # --- DPAD ---
            elif event.code == 'ABS_HAT0X': # Dpad Left/Right
                if event.state == -1:
                    v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
                elif event.state == 1:
                    v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
                else:
                    v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
                    v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
                    
            elif event.code == 'ABS_HAT0Y': # Dpad Up/Down
                # Inputs library tracks UP as -1, DOWN as 1
                if event.state == -1:
                    v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
                elif event.state == 1:
                    v_gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                else:
                    v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
                    v_gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

            # Send updates to the OS immediately after processing each hardware event
            v_gamepad.update()

except KeyboardInterrupt:
    print("\nExiting and cleaning up.")
