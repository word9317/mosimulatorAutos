import time
import keyboard
import vgamepad as vg

gamepad = vg.VX360Gamepad()

DEADZONE = 0
MAX = 32767


def get_axis(negative, positive):
    value = 0

    if keyboard.is_pressed(negative):
        value -= MAX
    if keyboard.is_pressed(positive):
        value += MAX

    return value


print("Keyboard -> Xbox 360 Controller")
print("Press CTRL+C to quit.")

while True:
    # -----------------
    # Left Stick (WASD)
    # -----------------
    lx = get_axis("a", "d")
    ly = get_axis("s", "w")  # Up is positive

    gamepad.left_joystick(x_value=lx, y_value=ly)

    # -----------------
    # Right Stick (J/L)
    # -----------------
    rx = get_axis("j", "l")
    gamepad.right_joystick(x_value=rx, y_value=0)

    # -----------------
    # Left Trigger
    # -----------------
    if keyboard.is_pressed("left shift"):
        gamepad.left_trigger(value=255)
    else:
        gamepad.left_trigger(value=0)

    # -----------------
    # Right Trigger
    # -----------------
    if keyboard.is_pressed("k"):
        gamepad.right_trigger(value=255)
    else:
        gamepad.right_trigger(value=0)
    if keyboard.is_pressed("space"):
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

    gamepad.update()

    time.sleep(0.005)