
# Note Application Project #

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Specify an absolute path for the JSON file
json_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "written_notes.json")

# Window Settings 

window = tk.Tk()
window.title("Note App")
window.geometry("600x600")
window.resizable(False, False)

# Style for notebook

style = ttk.Style()
style.configure("notebook.Tab", font=("Calibri", 15, "bold"))

notebook = ttk.Notebook(window, style="notebook.Tab")

#  Global variables for title_entry and content_text
title_entry = None
content_text = None

# Function to load previous notes to the notebook

def load_notes():
    try:
        with open(json_file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Load existing notes or initialize an empty dictionary
written_notes = load_notes()

notebook.pack(fill="both", expand=True)

# Function to add a new title/note to the notebook

def note_add(title="", content=""):
    global title_entry, content_text  # Access the global title_entry and content_text variables
    note_frame = ttk.Frame(notebook)
    note_frame.pack(fill="both", expand=True)
    notebook.add(note_frame, text=title)

    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W") # W refers to where the widget will be stuck toward e.g. West side of the notebook

    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="W")
    title_entry.insert("0", title)  # Set the title if provided
    title_entry.focus()  # Set focus on the title entry

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    # Use tk.Text for content with increased height
    content_text = tk.Text(note_frame, width=50, height=15)
    content_text.grid(row=1, column=1, padx=10, pady=10, sticky="W")
    content_text.insert("1.0", content)  # Set the content if provided

# Function to save a note to the notebook

def save():
    current_tab = notebook.select()
    main_title = title_entry.get()
    
    # Update the title in the tab
    notebook.tab(current_tab, text=main_title)

    main_content = content_text.get("1.0", "end-1c")

    written_notes[main_title] = main_content.strip()
    with open(json_file_path, "w") as f:
        json.dump(written_notes, f, indent=4)

# Create a global variable for content_text
content_text_entry = None

# Function to delete a note to the notebook

def delete():
    current_tab = notebook.index(notebook.select())
    note_title = notebook.tab(current_tab, "text")
    confirm = messagebox.askyesno("Delete Note?", f"Are you sure you want to delete {note_title}")
    if confirm:
        notebook.forget(current_tab)
        del written_notes[note_title]
        with open(json_file_path, "w") as f:
            json.dump(written_notes, f, indent=4)

# Loads previous saved notes to the notebook from the JSON file (REALLY IMPORTANT IF YOU ACTUALLY WANT TO LOAD A PREVIOUSLY SAVED NOTES)

def load_saved_notes():
    for title, content in written_notes.items():
        note_add(title, content)

# Buttons for the notebook

load_notes_button = ttk.Button(window, text="Load Notes", command=load_saved_notes)
load_notes_button.pack(side=tk.LEFT, padx=10, pady=10, ipadx=10, ipady=10)

button_new = ttk.Button(window, text="New Note", command=note_add)
button_new.pack(side=tk.LEFT, padx=10, pady=10, ipadx=10, ipady=10)

button_delete = ttk.Button(window, text="Delete Note", command=delete)
button_delete.pack(side=tk.LEFT, padx=10, pady=10, ipadx=10, ipady=10)

save_note_button = ttk.Button(window, text="Save Note", command=save)
save_note_button.pack(side=tk.LEFT, padx=10, pady=10, ipadx=10, ipady=10)

# Main Application Loop

window.mainloop()