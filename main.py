import ttkbootstrap as tb
from ttkbootstrap import *
from tkinter import filedialog
import os
import threading
import shutil

root = tb.Window().winfo_toplevel()
root.title("Create App and DMG")
root.geometry("500x500")
 
entry_frame = tb.Frame(master=root, padding=20)
entry_frame.pack(side=TOP, fill=X)

title = tb.Label(master=entry_frame, text="App & DMG creator", font=("Helvetica", 24, "bold"))
title.grid(row=0, columnspan=2, padx=20, pady=(10,20))

# Global variables to store file paths and app name
py_file_path = ""
icn_file_path = ""
app_name = ""

def browse_py_file():
    global py_file_path
    py_file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("Python File", "*.py"), ("All files", "*.*"))
    )
    if py_file_path:
        file_label.config(text=f"Python File: {py_file_path}")
        py_tick_label.config(text="✔️", foreground="green")  # Show green tick
    return py_file_path

def browse_icn_file():
    global icn_file_path
    icn_file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("Image File", "*.icns"), ("All files", "*.*"))
    )
    if icn_file_path:
        file_label.config(text=f"Icon File: {icn_file_path}")
        icn_tick_label.config(text="✔️", foreground="green")  # Show green tick
    return icn_file_path

def run_commands():
    global py_file_path, icn_file_path, app_name
    dmg_path = os.path.expanduser(f"~/Desktop/{app_name}.dmg")

    # Ensure previous DMG file is removed
    if os.path.exists(dmg_path):
        os.remove(dmg_path)

    # Ensure dist folder is cleaned
    dist_folder = os.path.join(os.getcwd(), "dist")
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)  # Remove all previous builds
    os.makedirs(dist_folder)  # Recreate dist folder

    # Construct pyinstaller command
    if my_option.get() == "M1":
        command = f"pyinstaller --name '{app_name}' --windowed --icon '{icn_file_path}' '{py_file_path}'"
    elif my_option.get() == "Intel":
        command = f"pyinstaller --target-arch=x86_64 --name '{app_name}' --windowed --icon '{icn_file_path}' '{py_file_path}'"
    else:
        details_label.config(text="Please select the Mac model")
        return

    os.system(command + ' -y')

    # Ensure the app exists before creating the DMG
    app_path = os.path.join(dist_folder, f"{app_name}.app")
    if not os.path.exists(app_path):
        details_label.config(text="App build failed, check PyInstaller output")
        create_button.config(state="normal")
        return

    # REMOVE the extra folder (dist/{app_name})
    extra_folder = os.path.join(dist_folder, app_name)
    if os.path.exists(extra_folder):
        shutil.rmtree(extra_folder)

    # Remove temporary DMG files before creating the final one
    temp_dmg_pattern = os.path.expanduser("~/Desktop/rw.*.dmg")
    os.system(f"rm -f {temp_dmg_pattern}")

    # Run create-dmg command to generate DMG with proper layout
    os.system(rf"""
    create-dmg \
      --volname "{app_name}" \
      --volicon "{icn_file_path}" \
      --window-pos 200 120 \
      --window-size 600 300 \
      --icon-size 100 \
      --icon "{app_name}.app" 175 120 \
      --hide-extension "{app_name}.app" \
      --app-drop-link 425 120 \
      --no-internet-enable \
      "{dmg_path}" \
      "dist"
    """)

    # Remove any remaining temporary DMG files
    os.system(f"rm -f {temp_dmg_pattern}")

    progress_bar.stop()
    progress_bar.pack_forget()

    details_label.config(text=f"DMG file created and saved on Desktop: {dmg_path}")
    print("Generated Command:", command)
    print("Selected Mac Model:", my_option.get())

    # Re-enable the Create button after the process is complete
    create_button.config(state="normal")
    py_browse_button.config(state="normal")
    browse_button.config(state="normal")

def create():
    global py_file_path, icn_file_path, app_name
    app_name = app_name_entry.get()  # Get the app name from the entry box
    if not app_name:
        details_label.config(text="Please enter an app name.")
        return
    if not py_file_path:
        details_label.config(text="Please select a Python file.")
        return
    if not icn_file_path:
        details_label.config(text="Please select an icon file.")
        return
    if not my_option.get():
        details_label.config(text="Please select the Mac model")
        return

    file_label.pack_forget()
    progress_bar.pack()
    progress_bar.start(10)

    # Disable the Create button to prevent multiple runs
    create_button.config(state="disabled")
    py_browse_button.config(state="disabled")
    browse_button.config(state="disabled")

    # Run the commands in a separate thread
    threading.Thread(target=run_commands, daemon=True).start()

# Frame Box
ques_frame = tb.LabelFrame(master=entry_frame, text="Enter the Details", padding=20)
ques_frame.grid(row=1, column=0, sticky="w", padx=25)

# Progress bar
progress_bar = ttk.Progressbar(root, mode='indeterminate')

# App Name Desc
tb.Label(master=ques_frame, text="Enter the App Name").grid(row=1, column=0, padx=10)

# User Entry Box
app_name_entry = tb.Entry(master=ques_frame)
app_name_entry.grid(row=1, column=1, sticky="w")

# Choose Python file Desc
tb.Label(master=ques_frame, text="Choose the Python file").grid(row=2, column=0, padx=10, pady=20)

# Python file browsing button
py_browse_button = tb.Button(master=ques_frame, text="Browse", width=19, command=browse_py_file, bootstyle=PRIMARY)
py_browse_button.grid(row=2, column=1, sticky="w")

# Green tick for Python file selection
py_tick_label = tb.Label(master=ques_frame, text="", font=("Helvetica", 12))
py_tick_label.grid(row=2, column=2, padx=10)

# Choose Icon file Desc
tb.Label(master=ques_frame, text="Choose the icns file").grid(row=3, column=0, padx=10, sticky="w")

# Icon file browsing button
browse_button = tb.Button(master=ques_frame, text="Browse", width=19, command=browse_icn_file, bootstyle=PRIMARY)
browse_button.grid(row=3, column=1, sticky="w")

# Green tick for Icon file selection
icn_tick_label = tb.Label(master=ques_frame, text="", font=("Helvetica", 12))
icn_tick_label.grid(row=3, column=2, padx=10)

# Choose Mac model Desc
tb.Label(master=ques_frame, text="Choose the mac model").grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Radio Buttons for Mac models
options = ["M1", "Intel"]
my_option = StringVar()
i = 4
for option in options:
    tb.Radiobutton(master=ques_frame, bootstyle="info", variable=my_option, text=option, value=option).grid(row=i, column=1, sticky="w", pady=5)
    i += 1

# Display the file path
file_label = tb.Label(root, text="No file selected", bootstyle=INFO)
file_label.pack(pady=10)

details_label = tb.Label(root, text="", bootstyle=SECONDARY)
details_label.pack(pady=10)

create_button = tb.Button(master=ques_frame, text="Create", width=19, command=create, bootstyle="success-outline")
create_button.grid(row=6, columnspan=2, pady=20)

root.mainloop()
