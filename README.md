# Ava
Ava is a tool that lets you change your sound input/output device quickly and easily!
If you bind the exe to a hotkey, it will cycle through your manually set list of devices to the next currently available one.

This works for both input and output devices with an option to set default communication device as well, thus retains all of the necessary functionality provided by all diff vanilla methods like "Volume Mixer", "Change System Sounds" and "Win+Ctrl+V".

This was made because Windows' built-in methods to do so are terrible.
- "Sound Mixer" doesnt set default "communication" microphone, just default microphone
- Audio device lists in Windows are often bloated (disabling them not always viable)
- The Ctrl + Win + V menu is buggy and doesn't overlay fullscreen games


TODO: hide admin window, CLI help

### installation with venv
0. install [python 3.12](https://www.python.org/downloads/)
    - enable "Add application directory to your system path"
1. download and extract [nircmd](https://www.nirsoft.net/utils/nircmd-x64.zip)
    - open `nircmd.exe` in the extracted folder
    - click `Copy to Windows Directory` then `Yes`
    - restart PC to ensure proper installation
2. download and extract the repo
3. open a Powershell window in this folder
    - method 1: open Powershell from Windows menu and enter `cd C:/PATH/TO/AVA
    - method 2: open from windows file explorer by shift-right click in an empty area in the Ava folder, click Open Powershell window here
4. Execute `python -m venv .venv` to create a virtual environment
5. Install all the required module with `./.venv/Scripts/pip.exe install -r requirements.txt`
6. Rename "config.py.example" to "config.py" (and edit with any text editor if desired)
7. To run from source: Execute `./LAUNCH.vbs <OPTIONS>` or `./.venv/Scripts/python.exe main.py <OPTIONS>`
    - `<OPTIONS>` are optional, check the [last section]() to see how to use them though

### configuration

0. search "System Sounds" in Windows menu, rename the devices you want to use here to have unique names
    - names can be 31 chars long max
    - don't use ' (' in names
    - no spaces at start or end in names (surrounding like "<u> ← these → </u>")
1. open `config.py` with any file editor
    1. enter all device names (without the parenthesis content)
        - get device names from System Sounds menu (enter without the parenthesis content)
        ex. `Sennheiser 560S (USB-C to 3.5mm Headphone Jack Adapter)` → `Sennheiser 560S`
        - split them into two seperate groups within `outputs` and `inputs` if you want
         -or- just put them all in the first ones, its fine if the second ones are empty
        - you can change these to have however many groups as you want, just make sure to put headphones/speakers in the `outputs[]` section and mics in the `inputs[]` section
    4. set `set_communication_device` to True iff you want this to cycle [Default Communication Device](https://superuser.com/questions/140978/whats-the-differnce-between-set-as-default-device-and-set-as-default-communi) as well
```python
# config.py
outputs = [
    [
        "Sennheiser 560S",
        ...
    ], [
        "AudioRelay",
        ...
    ]
]
inputs = [
    [
        "Behringer",
        ...
    ], [
      # this can be empty
    ]
]
set_communication_default = False
```



## Usage

```bash
usage: LAUNCH.vbs [-h] {input,output} [category]

Quickly change default audio device.

positional arguments:
  {input,output}  Cycle default input or output device.
  category        The name of the device to set as the default.

options:
  -h, --help      show this help message and exit
```
### usage in CMD/Powershell 
- `./LAUNCH.vbs output 0` cycles the first group of `outputs[]` in `config.py`
- `./LAUNCH.vbs input` cycles combined group of `inputs[]`

### bind to shortcut
this is how to bind Ava to a hotkey and make this start automatically when windows does

1. install [AutoHotkey v2](https://www.autohotkey.com/download/ahk-v2.exe)
2. open startup folder (win+R, type `shell:startup`, press enter)
3. right click > create shortcut:
    - target: `"C:\Program Files\AutoHotkey\v2\AutoHotkey64_UIA.exe" "C:\PATH\TO\AVA\shortcut.ahk"`
    - start in: `"C:\Program Files\AutoHotkey\v2"`
4. open `shortcut.ahk` with a text editor (ex. right-click > open with > notepad)
5. run `shortcut.ahk` to start the hotkey system in the background and test it