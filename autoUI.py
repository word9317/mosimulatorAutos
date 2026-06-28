import dearpygui.dearpygui as dpg
from autosystem import autoRecorder
import keyboard

AUTO = autoRecorder()

dpg.create_context()
dpg.create_viewport(title="MoSimulator Auto", width=420, height=400)

# an incredibly tuff theme(i give up on capitalizing comments
with dpg.theme() as theme:

    with dpg.theme_component(dpg.mvAll):

        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 6)

        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (28, 28, 32))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (45, 70, 120))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (60, 90, 150))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (80, 110, 180))

dpg.bind_theme(theme)

# helper functions cause im lazy
def update_ui():

    dpg.set_value("state", AUTO.getState())
    dpg.set_value("events", str(AUTO.getEventCount()))

keyboard.add_hotkey("\\", AUTO.startRecordingThread)
keyboard.add_hotkey("]", AUTO.playThread)
keyboard.add_hotkey("ctrl", AUTO.stop)

with dpg.window(label="AUTO MANAGER", width=400, height=380):
    dpg.add_text("MoSimulator AUTO System",color=(0, 180, 255))
    dpg.add_separator()
    dpg.add_text("Made by word9317")
    # status related stuff
    dpg.add_spacer(height=5)
    dpg.add_text("Current Status")
    dpg.add_text("Idle", tag="state")
    # key event tracker
    dpg.add_spacer(height=5)
    dpg.add_text("Recorded Events")
    dpg.add_text("0", tag="events")

    # buttons n stuff
    dpg.add_separator()
    # start auto recording
    dpg.add_button(
        label="Start Recording('\\' key)",
        width=-1,
        callback=lambda: AUTO.startRecordingThread()
    )
    # auto playback
    dpg.add_button(
        label="Play Auto(']' key)",
        width=-1,
        callback=lambda: AUTO.playThread()
    )
    # end current auto(ex if the auto messes up)
    dpg.add_button(
        label="Stop Auto('ctrl' key btw)",
        width=-1,
        callback=lambda: AUTO.stop()
    )

def refresh():
    update_ui()

# 10 updates per second
dpg.set_frame_callback(1, lambda: refresh())

dpg.set_viewport_always_top(True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

while dpg.is_dearpygui_running():
    update_ui()
    dpg.render_dearpygui_frame()

dpg.destroy_context()