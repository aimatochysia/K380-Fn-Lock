# import keyboard
import keyboard
import hid
import tkinter as tk
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE, LWA_ALPHA

# Constants Function Keys for Logitech K380 From:
# jergusg https://github.com/jergusg/k380-function-keys-conf/blob/master/k380_conf.c
K380_SEQ_FKEYS_ON = bytearray([0x10, 0xff, 0x0b, 0x1e, 0x00, 0x00, 0x00])
K380_SEQ_FKEYS_OFF = bytearray([0x10, 0xff, 0x0b, 0x1e, 0x01, 0x00, 0x00])
K380_VID = 0x46d
K380_PID = 0xb342
SEQ_LEN = 7
function_keys_enabled = False
is_alive = True


def hotkey_toggle():
    global function_keys_enabled
    global K380_SEQ_FKEYS_OFF
    global K380_SEQ_FKEYS_ON
    if function_keys_enabled:
        print("fn key off")
        toggle_function_keys(K380_SEQ_FKEYS_OFF)
        # display_box(False)
    else:
        print("fn key on")
        toggle_function_keys(K380_SEQ_FKEYS_ON)
        # display_box(True)
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


def set_clickthrough(self, hwnd):
    try:
        styles = GetWindowLong(hwnd, GWL_EXSTYLE)
        styles = WS_EX_LAYERED | WS_EX_TRANSPARENT
        SetWindowLong(hwnd, GWL_EXSTYLE, styles)
        SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA)
    except Exception as e:
        print(e)


def display_box(on_off):
    def lift_window():
        window.lift()
        window.after(10, lift_window)

    def fade_out(opacity=0.5):
        nonlocal window
        if opacity > 0:
            window.attributes('-alpha', opacity)
            window.after(30, fade_out, opacity - 0.05)
        else:
            window.destroy()

    root = tk.Tk()
    root.withdraw()
    window = tk.Toplevel()
    window.attributes('-topmost', True)
    window.attributes('-disabled', True)
    window.attributes('-toolwindow', True)
    window.wm_attributes("-transparentcolor", "white")
    window.attributes('-alpha', 0.5)
    window.overrideredirect(True)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 70
    window_height = 70
    window.geometry(f'{window_width}x{window_height}')
    x_position = (screen_width - window_width) // 2
    y_position = screen_height - window_height - 20
    window.geometry(f'+{x_position}+{y_position}')
    if on_off:
        label = tk.Label(window, text="Fn", font=(
            "Times New Roman", 24), fg="green")
    else:
        label = tk.Label(window, text="F̶n̶", font=(
            "Times New Roman", 24), fg="red")
    label.pack(expand=True)
    window.after(1000, fade_out)
    lift_window()
    window.mainloop()
    window.destroy()
    root.destroy()


# Main
keyboard.add_hotkey('ctrl + shift + alt', hotkey_toggle)
# bindings = [[['control', 'shift', 'alt'], None, hotkey_toggle]]
keyboard.wait()
print("Done Running")
