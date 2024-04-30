import tkinter as tk
import subprocess


def close_window():
    root.destroy()


def start_background_process():
    label.config(text="Copying . . .")
    button.config(text="Copying . . .", state=tk.DISABLED)
    root.update()
    subprocess.run(["startBackground.bat"])
    label.config(text="Done Copying!")
    button.config(text="OK", state=tk.NORMAL, command=close_window)


root = tk.Tk()
root.title("Copy Status")
root.iconbitmap("logo.ico")
label = tk.Label(root, text="Ready to copy")
label.pack(pady=10)
button = tk.Button(root, text="Start", width=10,
                   command=start_background_process)
button.pack()
root.mainloop()
