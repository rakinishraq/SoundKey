import ctypes, sys, subprocess, argparse, os
import gui, configparser, chime
from pprint import pprint

chime.theme('material')
chime.info()

config = configparser.ConfigParser()
config.read('config.ini')

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


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
                config['config'].get(device['Name'], device['Name']), \
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


def main(args):
    # ensure admin
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    # get list
    dir_path = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(dir_path, "audio.ps1")
    result = subprocess.run(["powershell", "-File", script_path], capture_output=True, text=True, startupinfo=startupinfo)
    result = parse_output(result.stdout)
    if args.verbose: pprint(result)

    # get index
    input_index = str(args.input_index)
    if input_index == '-1':
        if not args.verbose:
            input_index = gui.main(simplify(result, True))
        else:
            simplify(result)
            input_index = input("Select a device ~> ")
    print(f"\nSelected device ~> {input_index}")
    
    # valid index?
    if args.verbose: print("Indexes found: "+str(indexes))
    if input_index not in indexes:
        print("\nIndex not found, try again.\n")

        if args.input_index is not None:
            args.input_index = -1

        main(args)
    else:
        subprocess.run(["powershell", "-File", script_path, input_index], startupinfo=startupinfo)

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("input_index", type=int, nargs='?', default=-1, help="input index")
    args = parser.parse_args()

    main(args)