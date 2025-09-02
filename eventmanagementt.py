import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ---------- Database Setup ----------
conn = sqlite3.connect("event_management.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    participant_name TEXT NOT NULL,
    email TEXT NOT NULL,
    FOREIGN KEY(event_id) REFERENCES events(id)
)
""")

conn.commit()

# ---------- Functions ----------
def add_event():
    name = event_name_entry.get()
    date = event_date_entry.get()
    location = event_location_entry.get()

    if not (name and date and location):
        messagebox.showerror("Error", "All fields are required!")
        return

    cursor.execute("INSERT INTO events (name, date, location) VALUES (?, ?, ?)", (name, date, location))
    conn.commit()
    messagebox.showinfo("Success", "Event added successfully!")
    event_name_entry.delete(0, tk.END)
    event_date_entry.delete(0, tk.END)
    event_location_entry.delete(0, tk.END)
    load_events()

def register_participant():
    selected = event_list.focus()
    if not selected:
        messagebox.showerror("Error", "Please select an event!")
        return

    values = event_list.item(selected, "values")
    event_id = values[0]

    name = participant_name_entry.get()
    email = participant_email_entry.get()

    if not (name and email):
        messagebox.showerror("Error", "All fields are required!")
        return

    cursor.execute("INSERT INTO registrations (event_id, participant_name, email) VALUES (?, ?, ?)", (event_id, name, email))
    conn.commit()
    messagebox.showinfo("Success", f"{name} registered for {values[1]}!")
    participant_name_entry.delete(0, tk.END)
    participant_email_entry.delete(0, tk.END)

def load_events():
    for row in event_list.get_children():
        event_list.delete(row)

    cursor.execute("SELECT * FROM events")
    for row in cursor.fetchall():
        event_list.insert("", tk.END, values=row)

def view_registrations():
    selected = event_list.focus()
    if not selected:
        messagebox.showerror("Error", "Please select an event!")
        return

    values = event_list.item(selected, "values")
    event_id = values[0]

    cursor.execute("SELECT participant_name, email FROM registrations WHERE event_id = ?", (event_id,))
    participants = cursor.fetchall()

    if not participants:
        messagebox.showinfo("Registrations", "No participants registered yet.")
        return

    reg_list = "\n".join([f"{p[0]} ({p[1]})" for p in participants])
    messagebox.showinfo("Registrations", f"Participants for {values[1]}:\n\n{reg_list}")

# ---------- UI ----------
root = tk.Tk()
root.title("Event Management System")
root.geometry("700x500")

# Event Form
tk.Label(root, text="Event Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
event_name_entry = tk.Entry(root, width=30)
event_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Event Date:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
event_date_entry = tk.Entry(root, width=30)
event_date_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Event Location:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
event_location_entry = tk.Entry(root, width=30)
event_location_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Add Event", command=add_event).grid(row=3, column=0, columnspan=2, pady=10)

# Event List
columns = ("ID", "Name", "Date", "Location")
event_list = ttk.Treeview(root, columns=columns, show="headings", height=8)
for col in columns:
    event_list.heading(col, text=col)
event_list.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Participant Registration
tk.Label(root, text="Participant Name:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
participant_name_entry = tk.Entry(root, width=30)
participant_name_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Participant Email:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
participant_email_entry = tk.Entry(root, width=30)
participant_email_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Button(root, text="Register Participant", command=register_participant).grid(row=7, column=0, columnspan=2, pady=10)
tk.Button(root, text="View Registrations", command=view_registrations).grid(row=8, column=0, columnspan=2, pady=10)

# Load events on start
load_events()

root.mainloop()
