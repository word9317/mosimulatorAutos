import os
import tkinter as tk
from tkinter import messagebox, ttk
from autosystem import autoRecorder

# remind the user
messagebox.showinfo(
    "Make sure your settings are right!", 
    "Make sure MoSimulator is on Borderless fullscreen or windowed"
)

AUTO = autoRecorder()
AUTO.loadKeybindConfig()

autoName = "Auto"
autoPath = os.path.join("autos", f"{autoName}.json")
os.makedirs("./autos", exist_ok=True)


# functions

def changeAutoSaveName(event=None):
    global autoPath, autoName

    # Get string from input field
    autoName = auto_name_var.get().strip()

    if autoName == "":
        autoName = "Auto"

    autoPath = os.path.join("autos", f"{autoName}.json")
    
    # Sync entry box value just in case
    auto_name_var.set(autoName)
    print(autoPath)


def on_listbox_select(event):
    # Grab selected item from listbox
    selection = auto_listbox.curselection()
    if selection:
        selected_name = auto_listbox.get(selection[0])
        auto_name_var.set(selected_name)
        changeAutoSaveName()


def clearCurrentAuto():
    AUTO.clearAuto()
    events_label.config(text="0")
    saved_label.config(text="Current auto cleared")


def saveAutoAndUpdate():
    global autoPath

    if autoPath == "":
        autoPath = os.path.join("autos", f"{autoName}.json")

    AUTO.saveAuto(autoPath)
    refreshAutoList()
    saved_label.config(text=f"Saved: {autoName}.json")


def loadAuto():
    global autoPath

    if autoPath == "":
        autoPath = os.path.join("autos", f"{autoName}.json")

    if not os.path.exists(autoPath):
        saved_label.config(text="Auto not found!")
        return

    AUTO.loadAuto(autoPath)
    events_label.config(text=str(AUTO.getEventCount()))
    saved_label.config(text=f"Loaded: {autoName}.json")


def refreshAutoList():
    auto_listbox.delete(0, tk.END)
    if os.path.exists("autos"):
        for file in os.listdir("autos"):
            if file.endswith(".json"):
                auto_listbox.insert(tk.END, file[:-5])


def update_ui_loop():
    # Updates UI values roughly 10 times a second (every 100ms)
    try:
        state_label.config(text=AUTO.getState())
        events_label.config(text=str(AUTO.getEventCount()))
    except Exception:
        pass
    
    # Call this loop again in 100ms
    root.after(100, update_ui_loop)


# --- Settings Window ---
def update_button_labels():
    current_hotkeys = AUTO.getHotkeys()
    start_btn.config(text=f"Start Recording ('{current_hotkeys['record']}' key)")
    play_btn.config(text=f"Play Auto ('{current_hotkeys['play']}' key)")
    stop_btn.config(text=f"Stop Auto ('{current_hotkeys['stop']}' key)")

def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Keybind Settings")
    settings_win.geometry("420x380")
    settings_win.configure(bg=BG_COLOR)
    settings_win.attributes("-topmost", True)

    tk.Label(settings_win, text="Game Keybinds (comma-separated):", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    game_keys_var = tk.StringVar(value=", ".join(AUTO.getGameKeybinds()))
    tk.Entry(settings_win, textvariable=game_keys_var, bg="#2D2D30", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=1, relief="solid").pack(fill=tk.X, padx=10, pady=5)

    current_hotkeys = AUTO.getHotkeys()

    tk.Label(settings_win, text="Record Hotkey:", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    record_hk_var = tk.StringVar(value=current_hotkeys["record"])
    tk.Entry(settings_win, textvariable=record_hk_var, bg="#2D2D30", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=1, relief="solid").pack(fill=tk.X, padx=10, pady=5)

    tk.Label(settings_win, text="Play Hotkey:", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    play_hk_var = tk.StringVar(value=current_hotkeys["play"])
    tk.Entry(settings_win, textvariable=play_hk_var, bg="#2D2D30", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=1, relief="solid").pack(fill=tk.X, padx=10, pady=5)

    tk.Label(settings_win, text="Stop Hotkey:", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    stop_hk_var = tk.StringVar(value=current_hotkeys["stop"])
    tk.Entry(settings_win, textvariable=stop_hk_var, bg="#2D2D30", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=1, relief="solid").pack(fill=tk.X, padx=10, pady=5)

    def apply_settings():
        keys_text = game_keys_var.get()
        keys = [k.strip().lower() for k in keys_text.split(",") if k.strip()]
        AUTO.setGameKeybinds(keys)
        new_hotkeys = {
            "record": record_hk_var.get().strip(),
            "play": play_hk_var.get().strip(),
            "stop": stop_hk_var.get().strip()
        }
        AUTO.setHotkeys(new_hotkeys)
        update_button_labels()
        messagebox.showinfo("Settings", "Keybinds applied!", parent=settings_win)

    def save_config():
        apply_settings()
        AUTO.saveKeybindConfig()
        messagebox.showinfo("Settings", "Saved to keybinds_config.json", parent=settings_win)

    def load_config():
        AUTO.loadKeybindConfig()
        game_keys_var.set(", ".join(AUTO.getGameKeybinds()))
        hk = AUTO.getHotkeys()
        record_hk_var.set(hk["record"])
        play_hk_var.set(hk["play"])
        stop_hk_var.set(hk["stop"])
        update_button_labels()
        messagebox.showinfo("Settings", "Loaded from keybinds_config.json", parent=settings_win)

    btn_frame = tk.Frame(settings_win, bg=BG_COLOR)
    btn_frame.pack(fill=tk.X, padx=10, pady=15)

    for text, cmd in [("Apply", apply_settings), ("Save Config", save_config), ("Load Config", load_config)]:
        tk.Button(btn_frame, text=text, command=cmd, bg=BTN_COLOR, fg=TEXT_COLOR, activebackground=BTN_ACTIVE, activeforeground=TEXT_COLOR, relief="flat", bd=0, height=1, padx=10).pack(side=tk.LEFT, padx=3)


# --- Tkinter Window Setup ---
root = tk.Tk()
root.title("MoSimulator Auto")
root.geometry("450x650")
root.attributes("-topmost", True)  # Always on top

# Dark Palette Colors
BG_COLOR = "#1C1C20"       # (28, 28, 32)
BTN_COLOR = "#2D4678"      # (45, 70, 120)
BTN_ACTIVE = "#506EB4"     # (80, 110, 180)
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#00B4FF"   # (0, 180, 255)

root.configure(bg=BG_COLOR)

# Main container frame (mimics dpg.window padding)
main_frame = tk.Frame(root, bg=BG_COLOR, padx=15, pady=15)
main_frame.pack(fill=tk.BOTH, expand=True)


# --- UI Elements ---

# Header
title_lbl = tk.Label(main_frame, text="MoSimulator AUTO System", fg=ACCENT_COLOR, bg=BG_COLOR, font=("Arial", 14, "bold"))
title_lbl.pack(anchor="w", pady=(0, 2))

author_lbl = tk.Label(main_frame, text="Made by word9317", fg="#AAAAAA", bg=BG_COLOR, font=("Arial", 9))
author_lbl.pack(anchor="w", pady=(0, 10))

# Status Section
tk.Label(main_frame, text="Current Status", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
state_label = tk.Label(main_frame, text="Idle", fg=TEXT_COLOR, bg=BG_COLOR)
state_label.pack(anchor="w", pady=(0, 10))

tk.Label(main_frame, text="Recorded Events", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
events_label = tk.Label(main_frame, text="0", fg=TEXT_COLOR, bg=BG_COLOR)
events_label.pack(anchor="w", pady=(0, 10))

# Custom flat button generator to handle matching styles
def create_button(text, command):
    btn = tk.Button(
        main_frame, text=text, command=command, 
        bg=BTN_COLOR, fg=TEXT_COLOR, activebackground=BTN_ACTIVE, activeforeground=TEXT_COLOR,
        relief="flat", bd=0, height=2
    )
    # Give it a tiny bit of rounding simulation via padding style if needed, 
    # but basic flat styling works best out-of-the-box in Tkinter.
    return btn

# Control Buttons
start_btn = create_button("Start Recording ('\\' key)", AUTO.startRecordingThread)
start_btn.pack(fill=tk.X, pady=3)
play_btn = create_button("Play Auto (']' key)", AUTO.playThread)
play_btn.pack(fill=tk.X, pady=3)
stop_btn = create_button("Stop Auto ('ctrl' key btw)", AUTO.stop)
stop_btn.pack(fill=tk.X, pady=3)
create_button("Clear current Auto", clearCurrentAuto).pack(fill=tk.X, pady=3)
create_button("Keybind Settings", open_settings).pack(fill=tk.X, pady=3)

# Input Name Section
input_frame = tk.Frame(main_frame, bg=BG_COLOR)
input_frame.pack(fill=tk.X, pady=10)

tk.Label(input_frame, text="Auto Name: ", fg=TEXT_COLOR, bg=BG_COLOR).pack(side=tk.LEFT)
auto_name_var = tk.StringVar(value=autoName)
# Trace variable changes to mimic dpg callback on typing
auto_name_var.trace_add("write", lambda *args: changeAutoSaveName())

name_entry = tk.Entry(input_frame, textvariable=auto_name_var, bg="#2D2D30", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=1, relief="solid")
name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

# Save & Display Status
create_button("Save Auto", saveAutoAndUpdate).pack(fill=tk.X, pady=3)

saved_label = tk.Label(main_frame, text="Unsaved auto", fg="#E0A060", bg=BG_COLOR)
saved_label.pack(anchor="w", pady=5)

# Listbox for Auto Files
auto_listbox = tk.Listbox(main_frame, bg="#2D2D30", fg=TEXT_COLOR, selectbackground=BTN_COLOR, height=6, bd=0, highlightthickness=1, highlightbackground="#444444")
auto_listbox.pack(fill=tk.X, pady=5)
auto_listbox.bind("<<ListboxSelect>>", on_listbox_select)

create_button("Load Auto", loadAuto).pack(fill=tk.X, pady=3)


# --- App Startup ---
refreshAutoList()
update_button_labels()
root.after(100, update_ui_loop) # Start the 10Hz update loop
root.mainloop()