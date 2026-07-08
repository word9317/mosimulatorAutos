import dearpygui.dearpygui as dpg
from autosystem import autoRecorder
import keyboard
import os
# library to make popups look like windows, used for popup window
import ctypes
ctypes.windll.user32.MessageBoxW(0, "Make sure MoSimulator is on Borderless fullscreen or windowed", "Window Title", 1)

AUTO = autoRecorder()

autoName = "Auto"
autoPath = os.path.join("autos", f"{autoName}.json")

dpg.create_context()
dpg.create_viewport(title="MoSimulator Auto", width=450, height=650)
#saved auto directory
os.makedirs("./autos", exist_ok=True)

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

def changeAutoSaveName(sender, app_data):
    global autoPath
    global autoName

    autoName = app_data.strip()

    if autoName == "":
        autoName = "Auto"

    autoPath = os.path.join("autos", f"{autoName}.json")

    dpg.set_value("autoNameInput", autoName)

    print(autoPath)

def clearCurrentAuto():
    AUTO.clearAuto()

    dpg.set_value("events", "0")
    dpg.set_value("saved", "Current auto cleared")


    
def saveAutoAndUpdate():
    global autoPath

    if autoPath == "":
        autoPath = os.path.join("autos", f"{autoName}.json")

    AUTO.saveAuto(autoPath)

    refreshAutoList()

    dpg.set_value("saved", f"Saved: {autoName}.json")

def loadAuto():
    global autoPath

    if autoPath == "":
        autoPath = os.path.join("autos", f"{autoName}.json")

    if not os.path.exists(autoPath):
        dpg.set_value("saved", "Auto not found!")
        return

    AUTO.loadAuto(autoPath)
    dpg.set_value("events", str(AUTO.getEventCount()))
    dpg.set_value("saved", f"Loaded: {autoName}.json")

def refreshAutoList():

    files = []

    for file in os.listdir("autos"):
        if file.endswith(".json"):
            files.append(file[:-5])

    dpg.configure_item("autoList", items=files)



# helper functions cause im lazy
def update_ui():

    dpg.set_value("state", AUTO.getState())
    dpg.set_value("events", str(AUTO.getEventCount()))

keyboard.add_hotkey("\\", AUTO.startRecordingThread)
keyboard.add_hotkey("]", AUTO.playThread)
keyboard.add_hotkey("ctrl", AUTO.stop)

with dpg.window(label="AUTO MANAGER", width=420, height=600):
    dpg.add_text("MoSimulator AUTO System",color=(0, 180, 255))
    dpg.add_separator()
    dpg.add_text("Made by word9317(sircheetodust)")
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
    dpg.add_button(
        label="Clear current Auto",
        width=-1,
        callback=lambda: clearCurrentAuto()
    )
    dpg.add_separator()
    dpg.add_input_text(tag="autoNameInput", label="Auto Name", callback=changeAutoSaveName, on_enter=False)
    dpg.add_button(
        label="Save Auto",
        width=-1,
        callback=lambda: saveAutoAndUpdate()
    )
    dpg.add_text("Unsaved auto", tag="saved")
    dpg.add_listbox([], tag="autoList", width=-1, num_items=6, callback=lambda s, a: changeAutoSaveName(s, a))
    dpg.add_button(label="Load Auto", width=-1, callback=lambda: loadAuto())


# 10 updates per second
dpg.set_viewport_always_top(True)

dpg.setup_dearpygui()
dpg.show_viewport()
refreshAutoList()

while dpg.is_dearpygui_running():

    update_ui()

    dpg.render_dearpygui_frame()

dpg.destroy_context()
