import chime
import subprocess
import pyaudio
import argparse
import ctypes
import sys
from time import sleep
import os

if os.path.isfile('config.py'):
    import config
chime.theme("material")



def get_default(type):
    # Get default device name
    p = pyaudio.PyAudio()
    if type == "output":
        default_device_index = p.get_default_output_device_info()["index"]
    else:
        default_device_index = p.get_default_input_device_info()["index"]
    device_info = p.get_device_info_by_index(default_device_index)
    p.terminate()

    # Remove (...) suffix
    name = device_info["name"]
    if ' (' in name: name = name.split(' (', 1)[0]
    return name.strip()

def set_default(name):
    """Set default device by name excluding (...) suffix"""
    # default device
    subprocess.run([r'C:\Path\nircmd.exe', 'setdefaultsounddevice', name])
    sleep(1)

    # default communication device
    if config.set_communication_default:
        subprocess.run([r'C:\Path\nircmd.exe', 'setdefaultsounddevice', name, '2'])
        sleep(1)


def play_sound(success):
    # Play success or failure sound
    if success:
        print("Success!")
        chime.success()
    else:
        print("Failed!")
        chime.error()
    sleep(1)


def is_admin():
    """Return True if the given user is an administrator, False otherwise."""
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False


def main(args=None):
    chime.info()

    # Ensure admin
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit()

    # Parse args
    parser = argparse.ArgumentParser(description='Quickly change default audio device.')
    parser.add_argument('type', choices=['input', 'output'], help='Cycle default input or output device.')
    parser.add_argument('category', type=int, nargs='?', default=None, help='The name of the device to set as the default.')
    args = parser.parse_args(args)


    all_devices = config.outputs if args.type == "output" else config.inputs

    # Set devices[] to list of choices depending on --category flag presence
    if args.category is None:
        # Flatten the list of lists in config into one list
        devices = []
        for sublist in all_devices:
            for device in sublist:
                devices.append(device)
    else:
        # Get specific list in config
        devices = all_devices[args.category]

    # Get current default and initialize next_index
    next_index = -1
    if (old_name := get_default(args.type)) in devices:
        old_index = devices.index(old_name)
        if config.start_from_top:
            next_index = old_index
    else:
        old_index = len(devices) - 1

    # Loop through devices until default device changes
    while True:
        next_index = (next_index + 1) % len(devices)
        print("Trying: ", new_name := devices[next_index])
        set_default(new_name)

        if get_default(args.type) != old_name:
            # Device changed: success
            play_sound(success=True)
            break
        elif old_index == next_index:
            # Looped to current default device
            if config.start_from_top:
                # Skip original if start_from_top
                continue
            else:
                # If not start_from_top: failure
                play_sound(success=False)
                break

if __name__ == "__main__":
    default_args = ['output']
    main(sys.argv[1:] if len(sys.argv) > 1 else default_args)