import tkinter as tk
from tkinter import messagebox, Menu
import csv
import os
from datetime import datetime

APP_VERSION = "1.1.2"
AUTHOR = "zegron"
EMAIL = "matt@onetakemedia.net"
LICENSE_SNIPPET = "MIT License © 2025 zegron"

FILENAME = "time_log.csv"


# --- Core Functions ---

def log_action(action):
    """Log Punch In/Out actions to the CSV file."""
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

    from datetime import timedelta

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
        f"Time Clock App v{APP_VERSION}\n"
        f"Author: {AUTHOR}\n"
        f"Contact: {EMAIL}\n\n"
        f"{LICENSE_SNIPPET}\n\n"
        "A simple Windows desktop time tracker built with Python and Tkinter."
    )
    messagebox.showinfo("About", about_text)


# --- GUI Setup ---

root = tk.Tk()
root.title(f"Quick Time Clock v{APP_VERSION}")
root.geometry("340x280")


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
tk.Button(root, text="Exit", width=15, command=root.quit).pack(pady=5)


# --- Run App ---
root.mainloop()
