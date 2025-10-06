import tkinter as tk
from tkinter import messagebox, Menu
import csv
import os
from datetime import datetime, timedelta

# --- App Metadata ---
APP_VERSION = "1.1.5"  # Change this line only to update version everywhere
APP_NAME = f"Quick Time Clock v{APP_VERSION}"
AUTHOR = "zegron"
EMAIL = "matt@onetakemedia.net"
LICENSE_SNIPPET = "MIT License © 2025 zegron"

FILENAME = "time_log.csv"


# --- Core Functions ---

def get_last_action():
    """Read the last logged action from the CSV file, if any."""
    if not os.path.exists(FILENAME):
        return None
    try:
        with open(FILENAME, "r") as f:
            lines = f.readlines()
            if not lines:
                return None
            last_line = lines[-1].strip().split(",")
            if len(last_line) >= 2:
                return last_line[1].strip()
    except Exception:
        return None
    return None


def log_action(action):
    """Log Punch In/Out actions to the CSV file, preventing invalid sequences."""
    last_action = get_last_action()

    # Detect invalid sequence
    if action == "Punch In" and last_action == "Punch In":
        messagebox.showwarning("Warning", "You must Punch Out before punching in again.")
        return
    if action == "Punch Out" and last_action != "Punch In":
        messagebox.showwarning("Warning", "You must Punch In before punching out.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, action])
    messagebox.showinfo("Logged", f"{action} at {now}")


def view_log():
    """Display the entire log file contents."""
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found.")
        return
    with open(FILENAME, "r") as f:
        log = f.read()
    messagebox.showinfo("Time Log", log if log else "Log is empty.")


def calculate_hours():
    """Read the CSV file and calculate total hours."""
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found.")
        return

    entries = []
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            timestamp, action = row
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            entries.append((dt, action))

    sessions = []
    punch_in_time = None
    for dt, action in entries:
        if action == "Punch In":
            punch_in_time = dt
        elif action == "Punch Out" and punch_in_time:
            sessions.append((punch_in_time, dt))
            punch_in_time = None

    if not sessions:
        messagebox.showinfo("Hours Summary", "No completed sessions found.")
        return

    daily_totals = {}
    weekly_totals = {}
    all_time_total = 0.0

    for start, end in sessions:
        hours = (end - start).total_seconds() / 3600
        day = start.date()
        daily_totals[day] = daily_totals.get(day, 0) + hours
        # Week starts Sunday
        week_start = day - timedelta(days=day.weekday() + 1 if day.weekday() != 6 else 0)
        weekly_totals[week_start] = weekly_totals.get(week_start, 0) + hours
        all_time_total += hours

    summary = "Hours Summary\n" + "-" * 30 + "\n\n"
    summary += "Daily Totals:\n"
    for day in sorted(daily_totals):
        summary += f"{day}: {daily_totals[day]:.2f} hours\n"

    summary += "\nWeekly Totals (Sunday–Saturday):\n"
    for week in sorted(weekly_totals):
        summary += f"Week of {week}: {weekly_totals[week]:.2f} hours\n"

    summary += f"\nAll-Time Total: {all_time_total:.2f} hours"
    messagebox.showinfo("Hours Summary", summary)


def show_about():
    """Display app info in a popup window."""
    about_text = (
        f"{APP_NAME}\n"
        f"Author: {AUTHOR}\n"
        f"Contact: {EMAIL}\n\n"
        f"{LICENSE_SNIPPET}\n\n"
        "A simple Windows desktop time tracker built with Python and Tkinter."
    )
    messagebox.showinfo("About", about_text)


def on_exit():
    """Warn user if they are still punched in before exiting."""
    last_action = get_last_action()
    if last_action == "Punch In":
        confirm = messagebox.askyesno(
            "Still Punched In",
            "You are still punched in.\nAre you sure you want to exit?"
        )
        if not confirm:
            return  # Cancel exit
    root.destroy()  # Proceed with exit


# --- GUI Setup ---

root = tk.Tk()
root.title(APP_NAME)
root.geometry("340x300")  # slightly taller for footer label


# --- Digital Clock Display ---
clock_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"))
clock_label.pack(pady=5)


def update_clock():
    """Update the on-screen digital clock every second."""
    current_time = datetime.now().strftime("%I:%M:%S %p")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)


update_clock()


# --- Menu Bar ---
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Export Log (Coming Soon)")
menu_bar.add_cascade(label="File", menu=file_menu)

about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="About", menu=about_menu)


# --- Buttons ---
tk.Button(root, text="Punch In", width=15, command=lambda: log_action("Punch In")).pack(pady=5)
tk.Button(root, text="Punch Out", width=15, command=lambda: log_action("Punch Out")).pack(pady=5)
tk.Button(root, text="View Hours", width=15, command=calculate_hours).pack(pady=5)
tk.Button(root, text="View Log", width=15, command=view_log).pack(pady=5)
tk.Button(root, text="Exit", width=15, command=on_exit).pack(pady=5)

# --- Version Label (footer) ---
version_label = tk.Label(root, text=f"Version {APP_VERSION}", font=("Arial", 9), fg="gray")
version_label.pack(side="bottom", pady=3)


# --- Handle window close (X button) ---
root.protocol("WM_DELETE_WINDOW", on_exit)


# --- Run App ---
root.mainloop()
