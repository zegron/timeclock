import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime, timedelta

FILENAME = "time_log.csv"

def log_action(action):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, action])
    messagebox.showinfo("Logged", f"{action} at {now}")

def view_log():
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found")
        return
    with open(FILENAME, "r") as f:
        log = f.read()
    messagebox.showinfo("Time Log", log if log else "Log is empty")

def calculate_hours():
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found")
        return

    # Read log and pair Punch In / Punch Out
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
            punch_in_time = None  # Reset for next pair

    # Calculate daily totals
    daily_totals = {}
    weekly_totals = {}
    all_time_total = 0.0

    for start, end in sessions:
        hours = (end - start).total_seconds() / 3600  # precise hours
        day = start.date()
        daily_totals[day] = daily_totals.get(day, 0) + hours
        # Week starting Sunday
        week_start = day - timedelta(days=day.weekday() + 1 if day.weekday() != 6 else 0)
        weekly_totals[week_start] = weekly_totals.get(week_start, 0) + hours
        all_time_total += hours

    # Build summary text
    summary = "Hours Summary\n" + "-"*30 + "\n\n"
    summary += "Daily Totals:\n"
    for day in sorted(daily_totals):
        summary += f"{day}: {daily_totals[day]:.2f} hours\n"

    summary += "\nWeekly Totals (Sunday-Saturday):\n"
    for week in sorted(weekly_totals):
        summary += f"Week of {week}: {weekly_totals[week]:.2f} hours\n"

    summary += f"\nAll-Time Total: {all_time_total:.2f} hours"

    messagebox.showinfo("Hours Summary", summary)

# GUI Setup
root = tk.Tk()
root.title("Quick Time Clock")
root.geometry("300x250")

tk.Button(root, text="Punch In", width=15, command=lambda: log_action("Punch In")).pack(pady=5)
tk.Button(root, text="Punch Out", width=15, command=lambda: log_action("Punch Out")).pack(pady=5)
tk.Button(root, text="View Hours", width=15, command=calculate_hours).pack(pady=5)
tk.Button(root, text="View Log", width=15, command=view_log).pack(pady=5)
tk.Button(root, text="Exit", width=15, command=root.quit).pack(pady=5)

root.mainloop()
