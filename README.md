### why?
- allows hideing an audio device from this app without hiding it from other Windows menus
    - nickname any app "N/A" to hide it from the list on the next instance
- allows nicknaming
    - right-click any entry to nickname it
- allows CLI use, check `./LAUNCH.vbs --help` for details
    - `audio.ps1` works as standalone
    - `LAUNCH.vbs` is a decent method to run a Python file without showing a window
- shortcut compatible with fullscreen apps, escape to close
- can be bound to shortcut (detailed below)

### installation with venv
0. install [python 3.12](https://www.python.org/downloads/)
    - enable "Add application directory to your system path"
1. Clone the repo then open a terminal session in the folder or use `cd <path-to-Prisma>/Prisma`
    - for the former, shift-right click in an empty area in the folder, click Open Powershell window here
2. Execute `python -m venv .venv` to create a virtual environment
3. Install all the required module with `./.venv/Scripts/pip.exe install sv_ttk`
4. To run from source: Execute `./LAUNCH.vbs` or `./.venv/Scripts/python.exe main.py <ARGUMENTS>`

### bind to shortcut (+ hide admin popup)
- `!w` = Alt+W
- `+a` = Shift+A
- `^s` = Ctrl+S
- `;d` = Win+D

1. [install AutoHotkey v1](https://www.autohotkey.com/download/ahk-install.exe) making sure all context menu related options are enabled if present
2. ctrl+R to open Run, enter `shell:startup`
3. right-click > Show more options > New > AutoHotkey Script, enter any name with Empty selected and click Edit
4. enter the following, replace !v and path:
```ahk
#Requires AutoHotkey v1
!f::Run, D:\Projects\soundswitcher\LAUNCH.vbs
```
5. right-click `AnyName.ahk` > Show more options > Compile Script (GUI) > Change Base File to any `v1*.exe` > Convert
5. right-click > Show more options > Proprties then Compatibility tab > Run this program as an admin
6. double-click `AnyName.ahk`

### addresses problems
- "Sound Mixer" doesnt set default communication microphone, just default microphone
- all audio device lists in Windows are often too bloated (nickname N/A to hide)

### philosophy

speedrun a minimalist quick-access interface that also retains all of the necessary functionality provided by vanilla methods like "Volume Mixer", "Change System Sounds" and "Win+Ctrl+V"  
powershell script left as standalone for future better gui's  
besides readme changes, tkinter gui, python cli and powershell scripts written in < 18hrs

assumptions:
- audio.ps1 will always print all outputs before printing input (always been true so far)

handled:
- indexes not lining up as n+1 always (meaning not necessarily ordered)
- invalid index entered (re-execute)
- sound devices changing before re-execution (calculate list again instead of saving)