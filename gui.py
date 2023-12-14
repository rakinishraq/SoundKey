import tkinter
from tkinter import ttk
import tkinter.simpledialog
import sv_ttk

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

selected_index = None
def closer(root, ret=None):
    global selected_index
    root.destroy()
    selected_index = ret


buttons = {}
def update_config(key, name, root):
    root.withdraw()

    # Temporarily unbind the FocusOut event
    root.unbind("<FocusOut>")

    # Open a popup window for user input
    new_value = tkinter.simpledialog.askstring("Input", "Enter new value for " + name)

    if new_value is not None:
        # Update the config.ini file
        config['alias'][name] = new_value

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
        buttons[key].config(text=new_value)

    # Rebind the FocusOut event
    root.bind("<FocusOut>", lambda _e: closer(root))

    # unhide and focus
    root.deiconify()
    root.focus_force()


def main(data):
    root = tkinter.Tk()
    root.title('Audio Device')
    root.overrideredirect(True)
    
    num_columns = int(config['gui']['columns'])
    gap = float(config['gui']['gap'])/200

    # center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (int(config['gui']['width']) / 2)
    y = (screen_height / 2) - (int(config['gui']['height']) / 2)
    root.geometry(f"700x200+{int(x)}+{int(y)}")

    # Escape to close
    root.bind("<Escape>", lambda _e: closer(root))
    root.bind("<FocusOut>", lambda _e: closer(root))

    if config.getboolean('gui', 'transparent'):
        root.wm_attributes('-transparentcolor', "#1c1c1c")
    root.wm_attributes("-topmost", 1)

    # Create two frames for the two grids
    frame1 = ttk.Frame(root)
    frame2 = ttk.Frame(root)

    for i in range(num_columns):
        frame1.grid_columnconfigure(i, weight=1)
        frame2.grid_columnconfigure(i, weight=1)

    # Create a button for each item in data
    for i, (key, (name, nickname, default, is_output)) in enumerate(data.items()):
        if default: continue

        frame = frame1 if is_output else frame2
        place = len(frame.grid_slaves())

        button = ttk.Button(frame, text=nickname, width=10,
                            command=lambda key=key: closer(root, key))

        # Bind the right-click event to the update_config function
        button.bind('<Button-3>', lambda event, key=key, name=name: update_config(key, name, root))

        button.grid(row=place // num_columns * 2, column=place % num_columns, sticky='nsew')

        buttons[key] = button
    

    # Arrange the frames in the root window
    frame1.place(relx=0, rely=0, relwidth=0.5-gap, relheight=1)
    #frame1 label = default[1]
    frame2.place(relx=0.5+gap, rely=0, relwidth=0.5-gap, relheight=1)
    #frame2 label = default[0]


    sv_ttk.set_theme("dark")
    root.focus_force()
    root.mainloop()
    return selected_index

if __name__ == "__main__":
    main({
        '1': ["Test", "Test", True, True],
        '2': ["Test", "Test", False, True],
        '3': ["Test", "Test", True, False],
        '4': ["Test", "Test", False, False],
    })