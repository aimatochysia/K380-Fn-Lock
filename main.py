import keyboard
import hid
import tkinter as tk
# Constants Function Keys for Logitech K380 From:
# jergusg https://github.com/jergusg/k380-function-keys-conf/blob/master/k380_conf.c
K380_SEQ_FKEYS_ON = bytearray([0x10, 0xff, 0x0b, 0x1e, 0x00, 0x00, 0x00])
K380_SEQ_FKEYS_OFF = bytearray([0x10, 0xff, 0x0b, 0x1e, 0x01, 0x00, 0x00])
K380_VID = 0x46d
K380_PID = 0xb342
SEQ_LEN = 7
function_keys_enabled = False


def hotkey_toggle():
    global function_keys_enabled
    global K380_SEQ_FKEYS_OFF
    global K380_SEQ_FKEYS_ON
    if function_keys_enabled:
        print("fn key off")
        toggle_function_keys(K380_SEQ_FKEYS_OFF)
    else:
        print("fn key on")
        toggle_function_keys(K380_SEQ_FKEYS_ON)
    function_keys_enabled = not function_keys_enabled


def toggle_function_keys(seq):
    global K380_VID
    global K380_PID
    global SEQ_LEN
    handle = None
    try:
        devs = hid.enumerate(K380_VID, K380_PID)
        for cur_dev in devs:
            if cur_dev['usage'] == 1 and cur_dev['usage_page'] == 65280:
                handle = hid.device()
                handle.open_path(cur_dev['path'])
                if handle.write(seq) != SEQ_LEN:
                    print("Error: Failed to toggle function keys")
                break
    except Exception as e:
        print("Exception:", e)
    finally:
        if handle:
            handle.close()


def display_message():
    window = tk.Toplevel()
    window.attributes('-topmost', True)
    window.overrideredirect(True)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 100
    window_height = 50
    window.geometry(f'{window_width}x{window_height}')
    x_position = (screen_width - window_width) // 2
    y_position = screen_height - window_height
    window.geometry(f'+{x_position}+{y_position}')
    label = tk.Label(window, text="Fn", font=("Helvetica", 12))
    label.pack(expand=True)
    window.after(1000, window.destroy)
    window.mainloop()


# Main
display_box()
# keyboard.add_hotkey('ctrl + shift + alt', hotkey_toggle)
# keyboard.wait()
print("Done Running")
