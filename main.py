import tkinter as tk
from tkinter import messagebox, font
import json
import os
from datetime import datetime

# List of daily tasks
# Example tasks
FIXED_TASKS = [
    "Exercise",
    "Read for 30 minutes",
    "Study school stuff",
    "Work on school project",
    "Clean",
    "Plan tomorrow"
]

# File to store task statuses
TODO_FILE = "daily_task_status.json"

def reset_task_status():
    task_status = {task: False for task in FIXED_TASKS}  # Marks all tasks to incomplete
    save_task_status(task_status)

def load_task_status():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            task_status = json.load(file)
    else:
        task_status = {task: False for task in FIXED_TASKS}
        save_task_status(task_status)  # Save status

    # Check tasks are loaded
    for task in FIXED_TASKS:
        if task not in task_status:
            task_status[task] = False  # Mark tasks incomplete if not found

    return task_status

def save_task_status(task_status):
    with open(TODO_FILE, 'w') as file:
        json.dump(task_status, file)

def check_reset_time():
    now = datetime.now()
    if os.path.exists(TODO_FILE):
        last_modified = datetime.fromtimestamp(os.path.getmtime(TODO_FILE))
    else:
        reset_task_status()  # Create file if doesn't exist
        return

    if now.hour >= 0 and last_modified.date() < now.date():
        reset_task_status()

def update_task_list():
    check_reset_time()
    task_status = load_task_status()
    for idx, task in enumerate(FIXED_TASKS):
        task_var = task_vars[idx]
        task_var.set(task_status.get(task, False))

def toggle_task_completion(idx):
    """Toggle the completion status of a task."""
    task_status = load_task_status()
    task = FIXED_TASKS[idx]
    task_status[task] = not task_status[task]  # Toggles completion status
    save_task_status(task_status)
    update_task_list()

#Manually reset all tasks button function
def reset_all_tasks():
    reset_task_status()
    update_task_list()

# GUI setup stuff
root = tk.Tk()
root.title("Daily To-Do List")
root.geometry("450x400")
root.config(bg="#f5f5f5")
root.iconbitmap('icon.ico')

# Header stuff
header_font = font.Font(family="Helvetica", size=16, weight="bold")
header_label = tk.Label(root, text="Daily To-Do List", font=header_font, bg="#f5f5f5", fg="#4a4a4a")
header_label.pack(pady=10)

# Scrollable stuff
frame_tasks = tk.Frame(root, bg="#f5f5f5")
frame_tasks.pack(pady=10, padx=10, fill="both", expand=True)

canvas = tk.Canvas(frame_tasks, bg="#f5f5f5", highlightthickness=0)
scrollbar = tk.Scrollbar(frame_tasks, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Checkboxes
task_vars = []
checkbox_font = font.Font(family="Helvetica", size=12)

# Create the checkboxes for each fixed task
for idx, task in enumerate(FIXED_TASKS):
    task_var = tk.BooleanVar()
    task_vars.append(task_var)
    checkbox = tk.Checkbutton(scrollable_frame, text=task, variable=task_var, command=lambda idx=idx: toggle_task_completion(idx), font=checkbox_font, bg="#f5f5f5", fg="#333333", selectcolor="#d4edda")
    checkbox.pack(anchor="w", padx=5, pady=2)

# Reset All Tasks Button
reset_button = tk.Button(root, text="Reset All Tasks", command=reset_all_tasks, bg="#ff6b6b", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
reset_button.pack(pady=15)

# Main running/updating stuff

update_task_list()


root.mainloop()
