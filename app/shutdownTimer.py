import os
import customtkinter as ctk
from tkinter.messagebox import showerror, showwarning, askokcancel
import ctypes
from pystray import MenuItem as item, Icon
from PIL import Image

# Set appearance and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Shutdown Timer")
root.resizable(False, False)
root.iconbitmap("assets/icon.ico") # Icon path

# App sizing and center window
app_width = 400
app_height = 350
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinates = (screen_width - app_width) / 2
y_coordinates = (screen_height - app_height) / 2
root.geometry(f"{app_width}x{app_height}+{int(x_coordinates)}+{int(y_coordinates)}")

global prevent_sleep
prevent_sleep = False

# Shutdown button function
def shutdown_clicked():
    global prevent_sleep
    if entry_hour.get() or entry_minute.get():
        hour = int(entry_hour.get() or 0)
        minute = int(entry_minute.get() or 0)
        seconds = (hour * 3600) + (minute * 60)

        # Prevent sleep
        if disable_sleep.get():
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
            prevent_sleep = True

        command = "shutdown -s -t {}".format(seconds)        
        shutdown_error = os.system(command)
        # Check for any command error
        if shutdown_error:
            showerror(title="Error", message="Command could not be executed!")
        else:
            shutdown_button.configure(fg_color="#2AA526", hover_color="#1A8A1F", state="disabled", text="Timer Started")
            cancel_button.configure(fg_color="#DB282C", hover_color="#B71C2B", state="normal", text="Cancel Shutdown")

    else:
        showwarning(title="Error", message="Input Required!")

# Cancel the shutdown button function
def shutdown_cancel_clicked():
    global prevent_sleep
    # Cancel prevent sleep
    if prevent_sleep:
        ctypes.windll.kernel32.SetThreadExecutionState(0x00000000)
        prevent_sleep = False

    cancel_error = os.system('shutdown -a') 
    # Check for any command error
    if cancel_error:
        showerror(title="Error", message="Command could not be executed!")
    else:
        cancel_button.configure(fg_color="#6c757d", hover_color="#B71C2B", state="disabled", text="Shutdown Canceled")
        shutdown_button.configure(fg_color="#3B8ED0", hover_color="#36719F", state="normal", text="Start Timer")

# Title label
label = ctk.CTkLabel(root, text="Set Shutdown Timer", font=('Roboto', 16))
label.pack(padx=20, pady=20)

# Hour input
entry_hour = ctk.CTkEntry(root, placeholder_text="Hour")
entry_hour.pack(padx=20, pady=10)

# Minute input
entry_minute = ctk.CTkEntry(root, placeholder_text="Minute")
entry_minute.pack(padx=20, pady=10)

# Create a Checkbutton to disable sleep
disable_sleep = ctk.BooleanVar()
disable_sleep_checkbutton = ctk.CTkCheckBox(root, text="Keep Computer Awake", variable=disable_sleep)
disable_sleep_checkbutton.pack(padx=20, pady=10)

# Shutdown button
shutdown_button = ctk.CTkButton(root, text="Start Timer", command=shutdown_clicked)
shutdown_button.pack(padx=20, pady=10)

# Cancel button
cancel_button = ctk.CTkButton(root, text="Cancel Shutdown", fg_color="#DB282C", hover_color="#B71C2B", command=shutdown_cancel_clicked)
cancel_button.pack(padx=20, pady=10)

# Close app function
def on_closing():
    global prevent_sleep
    if askokcancel("Quit", "Are you sure you want to exit and cancel the shutdown timer?"):
        if prevent_sleep:
            ctypes.windll.kernel32.SetThreadExecutionState(0x00000000)
        os.system('shutdown -a')
        root.destroy()

# Menu quit function
def quit_window(icon, item):
    icon.stop()
    root.after(0,root.deiconify)
    root.after(500,on_closing)

def show_window(icon, item):
    icon.stop()
    root.after(0,root.deiconify)

def withdraw_window():
    root.withdraw()
    image = Image.open("assets/icon.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = Icon("name", image, "title", menu)
    icon.run()

root.protocol("WM_DELETE_WINDOW", withdraw_window)

root.mainloop()
