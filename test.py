import tkinter as tk
import tkinter.ttk as ttk
import time
def show_osd_message(message, duration=3):
    root = tk.Tk()
    root.overrideredirect(True)
    root.withdraw()
    osd_window = tk.Toplevel(root)
    osd_window.geometry("100x100")
    osd_window.configure(bg="#0f0f0f")
    osd_window.overrideredirect(True)
    root.attributes('-topmost',True)
    root.attributes('-alpha',0)
    root.attributes('-alpha',0.5)
    screen_width = osd_window.winfo_screenwidth()
    screen_height = osd_window.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = screen_height - 120
    osd_window.geometry('+{}+{}'.format(x_position, y_position))
    label = ttk.Label(osd_window, text=message, font=("Arial",20), foreground="#F0F8FF", background="#0f0f0f")
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

show_osd_message("Fn", duration=1.0)
time.sleep(2)
show_osd_message("Fn", duration=1.0)