# import keyboard
import keyboard
import hid
import tkinter as tk
import tkinter.ttk as ttk
import win32gui
import win32con

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
        show_osd_message("Fn",1,False)
    else:
        print("fn key on")
        toggle_function_keys(K380_SEQ_FKEYS_ON)
        show_osd_message("Fn",1,True)
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


def setClickthrough(hwnd):
    try:
        styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)


# def display_box(on_off):
#     def lift_window():
#         window.lift()
#         window.after(10, lift_window)

#     def fade_out(opacity=0.5):
#         nonlocal window
#         if opacity > 0:
#             window.attributes('-alpha', opacity)
#             window.after(30, fade_out, opacity - 0.05)
#         else:
#             window.destroy()

#     root = tk.Tk()
#     root.withdraw()
#     window = tk.Toplevel()
#     window.attributes('-topmost', True)
#     window.attributes('-disabled', True)
#     window.attributes('-toolwindow', True)
#     window.wm_attributes("-transparentcolor", "white")
#     window.attributes('-alpha', 0.5)
#     window.overrideredirect(True)
#     screen_width = window.winfo_screenwidth()
#     screen_height = window.winfo_screenheight()
#     window_width = 70
#     window_height = 70
#     window.geometry(f'{window_width}x{window_height}')
#     x_position = (screen_width - window_width) // 2
#     y_position = screen_height - window_height - 20
#     window.geometry(f'+{x_position}+{y_position}')
#     if on_off:
#         label = tk.Label(window, text="Fn", font=(
#             "Times New Roman", 24), fg="green")
#     else:
#         label = tk.Label(window, text="F̶n̶", font=(
#             "Times New Roman", 24), fg="red")
#     label.pack(expand=True)
#     window.after(1000, fade_out)
#     lift_window()
#     window.mainloop()
#     window.destroy()
#     root.destroy()
    
def show_osd_message(message, duration=3, on_off = False):
    # Create a root window and immediately withdraw it
    root = tk.Tk()
    root.overrideredirect(True)
    root.withdraw()
    osd_window = tk.Toplevel(root)
    osd_window.geometry("100x100")
    osd_window.configure(bg="#0f0f0f")
    osd_window.overrideredirect(True)
    root.attributes('-topmost',True)
    root.attributes('-alpha',0)
    osd_window.attributes('-alpha',0.5)
    screen_width = osd_window.winfo_screenwidth()
    screen_height = osd_window.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = screen_height - 120
    osd_window.geometry('+{}+{}'.format(x_position, y_position))
    setClickthrough(osd_window.winfo_id())
    if on_off == True:
        label = ttk.Label(osd_window, text=message, font=("Arial",20), foreground="##c2ddff", background="#0f0f0f")
    else:
        label = ttk.Label(osd_window, text=message, font=("Arial",20), foreground="##ffc2c2", background="#0f0f0f")
    label.place(relx=0.5,rely=0.5, anchor="center")
    label.pack(pady=(30,0))
    fade_duration = duration
    def fade_out():
        current_opacity = osd_window.attributes("-alpha")
        if current_opacity > 0:
            current_opacity -= .01
            osd_window.attributes("-alpha", current_opacity)
            osd_window.after(20, fade_out)
    try:
        osd_window.after(int(fade_duration * 100), fade_out)
    except:
        pass
    osd_window.after(int(duration * 1000), lambda: (osd_window.destroy(), root.destroy()))
    osd_window.mainloop()

# Main
keyboard.add_hotkey('ctrl + shift + alt', hotkey_toggle)
# bindings = [[['control', 'shift', 'alt'], None, hotkey_toggle]]
keyboard.wait()
print("Done Running")
