# MosimulatorAutos
One limitation is that the game currently does not include an autonomous period, where a robot follows a pre-programmed routine. This project recreates that behavior by recording and replaying keyboard inputs.

## Overview
[Demo Video](https://youtu.be/ruoJCHwV8D4)
### Features
 - Recording Auto stage(first 20 seconds of match)
 - Auto playback
 - Auto saving and loading from json files

### Caveats
- Replay accuracy depends on starting in the same position.
- Camera orientation should remain unchanged.
- Stable frame rates improve replay accuracy.
- Keyboard layout should match the one used during recording(This application uses default layout)

## Usage
### Installation

#### Requirements

- Windows 10/11
- MoSimulator
- Keyboard controls enabled

#### Prebuilt .exe file
1. Download from releases
2. Unzip mosimautosystem.zip
3. Run moSimAuto.exe

#### Source code method
1. Install python([Download available here](https://www.python.org/downloads/))
2. Install packages:
```
pip install -r requirements.txt
```
3. Run the program
```
python main.py
```
### TUTORIAL:
[text](https://youtu.be/8YWMb9f-9nQ)

### Shortcuts
### IMPORTANT
Make sure your game is on borderless instead of fullscreen.

| Key | Action |
|------|--------|
| `\` | Record an auto |
| `]` | Play the recorded auto |
| `Ctrl` | Stop playback immediately(if something goes wrong) |

## Changelog
### 1.0 - Initial release
### 1.1 - Minor fixes
### 1.2 - Full UI transition to tkinter, Change keybinds
 - Transitioned to tkinter
 - Added some tips into the application(borderless mode and keyboard shortcuts)
 - Added ability to change keybinds

## Credits

Created by word9317.

MoSimulator is developed by the MoSimulator team. This project is an unofficial community tool and is not affiliated with or endorsed by the MoSimulator developers.
