import ctypes, sys, subprocess, argparse, os
import gui, configparser, chime, keyboard
from pprint import pprint

# subprocess args
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# sound effect
chime.theme('material')
chime.info()

def is_admin():
    """Return True if the given user is an administrator, False otherwise."""
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

# read config
config = configparser.ConfigParser()
config.read('config.ini')


def main():
    """
    First step is to ensure this process is admin then get the initial device list.
    If in daemon mode, start listening for autohotkey signal to spawn a subprocess window.
    Otherwise, spawn window as subprocess then quit.
    """
    # ensure admin
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="visible subprocess terminal windows", action="store_true")
    args = parser.parse_args()

    keyboard.add_hotkey(config['daemon']['hotkey'], lambda: spawn(args))
    keyboard.wait()


def spawn(args):
    print('CapsLock + V pressed')

    # get list
    dir_path = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(dir_path, "audio.ps1")
    result = subprocess.run(["powershell", "-File", script_path], capture_output=True, text=True, startupinfo=startupinfo)
    result = parse_output(result.stdout)
    pprint(result)
    subprocess.run(["powershell", "-File", script_path, input_index], startupinfo=startupinfo)
        

indexes = []
def parse_output(output):
    global indexes
    devices = []
    device = {}

    for line in output.splitlines():
        if line:
            key, value = line.split(':', 1)
            device[key := key.strip()] = (value := value.strip())
            if key == "Index": indexes.append(value)
        else:
            if device:
                devices.append(device)
                device = {}

    if device:
        devices.append(device)

    return devices


def simplify(parsed, no_print=False):
    lines = []
    output = {}

    try:
        heading_shown = False
        lines.append("# Outputs\n")

        for device in parsed:
            default, default_comm, name, index, is_output = \
                "X" if device['Default'] == 'True' else "_", \
                "X" if device['DefaultCommunication'] == 'True' else "_", \
                config['nickname'].get(device['Name'], device['Name']), \
                device['Index'], device['Type'] == 'Playback'
            
            if not is_output and not heading_shown:
                heading_shown = True
                lines.append("\n# Inputs")

            if name == 'N/A':
                continue

            lines.append(f"[{default}] [{default_comm}] {index}. {name}")
            output[index] = [device['Name'], name, default != '_', is_output]
        
        if not no_print: print('\n'.join(lines))
        return output
    except Exception as e:
        print("Successfully parsed: "+str(lines))
        print(e)


if __name__ == "__main__":
    main()