import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

FILENAME = "time_log.csv"

def log_action(action):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, action])
    messagebox.showinfo("Logged", f"{action} at {now}")

def undo_last(n=1):
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found")
        return
    with open(FILENAME, "r") as f:
        lines = f.readlines()
    if len(lines) <= n:
        messagebox.showwarning("Error", "Not enough records to undo")
        return
    with open(FILENAME, "w") as f:
        f.writelines(lines[:-n])
    messagebox.showinfo("Undo", f"Removed last {n} record(s)")

def view_log():
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found")
        return
    with open(FILENAME, "r") as f:
        log = f.read()
    messagebox.showinfo("Time Log", log if log else "Log is empty")

# GUI Setup
root = tk.Tk()
root.title("Quick Time Clock")
root.geometry("300x200")

tk.Button(root, text="Punch In", width=15, command=lambda: log_action("Punch In")).pack(pady=5)
tk.Button(root, text="Punch Out", width=15, command=lambda: log_action("Punch Out")).pack(pady=5)
tk.Button(root, text="Undo Last", width=15, command=lambda: undo_last(1)).pack(pady=5)
tk.Button(root, text="Undo Two", width=15, command=lambda: undo_last(2)).pack(pady=5)
tk.Button(root, text="View Log", width=15, command=view_log).pack(pady=5)
tk.Button(root, text="Exit", width=15, command=root.quit).pack(pady=5)

root.mainloop()
