import csv
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk

# CSV கோப்பின் பெயர்
CSV_FILE = "attendees.csv"

# கோப்பு இல்லை என்றால் Date & Time தலைப்புடன் புதிய கோப்பை உருவாக்குதல்
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Email", "Phone", "Registered Time"])


# 1. Function to Register Attendee (நேரத்துடன் சேமிக்க)
def register_attendee():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if name == "" or email == "" or phone == "":
        messagebox.showwarning(
            "Input Error", "Please fill in all the required fields!"
        )
        return

    # தற்போதைய தேதி மற்றும் நேரத்தைப் பெறுதல் (எ.கா: 2026-10-07 14:30:45)
    registered_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # அடுத்த ID எண்ணைக் கண்டறிதல்
    next_id = 1
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                next_id = int(reader[-1][0]) + 1

    # CSV கோப்பில் விவரங்கள் + நேரத்தைச் சேர்த்தல்
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([next_id, name, email, phone, registered_time])

    messagebox.showinfo("Success", "Attendee Registered Successfully!")

    # Input பாக்ஸ்களை காலியாக்குதல்
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


# 2. Function to Delete Selected Attendee
def delete_attendee(tree):
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showwarning(
            "Selection Error", "Please select a record to delete!"
        )
        return

    record = tree.item(selected_item)
    selected_id = str(record["values"][0])

    confirm = messagebox.askyesno(
        "Confirm Delete", "Are you sure you want to delete this attendee?"
    )

    if confirm:
        rows = []
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in rows:
                if row and row[0] != selected_id:
                    writer.writerow(row)

        tree.delete(selected_item)
        messagebox.showinfo("Success", "Attendee deleted successfully!")


# 3. Function to View Data (Registered Time உட்பட பார்க்க)
def view_attendees():
    view_window = tk.Toplevel(root)
    view_window.title("Registered Attendees List")
    view_window.geometry("700x380")

    # Table (Treeview) உருவாக்கம் - Registered Time நெடுவரிசை சேர்க்கப்பட்டுள்ளது
    tree = ttk.Treeview(
        view_window,
        columns=("ID", "Name", "Email", "Phone", "Registered Time"),
        show="headings",
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Phone", text="Phone")
    tree.heading("Registered Time", text="Registered Time")

    tree.column("ID", width=40, anchor="center")
    tree.column("Name", width=120)
    tree.column("Email", width=180)
    tree.column("Phone", width=110)
    tree.column("Registered Time", width=150, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # CSV கோப்பில் இருந்து தரவை ஏற்றுதல்
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip Header
            for row in reader:
                if row:
                    tree.insert("", tk.END, values=row)

    # Delete Button
    delete_button = tk.Button(
        view_window,
        text="Delete Selected Attendee",
        font=("Arial", 10, "bold"),
        bg="#f44336",
        fg="white",
        command=lambda: delete_attendee(tree),
    )
    delete_button.pack(pady=10)


# 4. GUI Layout Creation
root = tk.Tk()
root.title("Event Registration System")
root.geometry("400x350")
root.configure(bg="#f0f0f0")

title_label = tk.Label(
    root,
    text="Event Registration Form",
    font=("Arial", 16, "bold"),
    bg="#f0f0f0",
)
title_label.pack(pady=10)

# Name Input
name_label = tk.Label(root, text="Full Name:", font=("Arial", 10), bg="#f0f0f0")
name_label.pack(anchor="w", padx=40)
name_entry = tk.Entry(root, width=40)
name_entry.pack(pady=5)

# Email Input
email_label = tk.Label(root, text="Email:", font=("Arial", 10), bg="#f0f0f0")
email_label.pack(anchor="w", padx=40)
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

# Phone Input
phone_label = tk.Label(root, text="Phone Number:", font=("Arial", 10), bg="#f0f0f0")
phone_label.pack(anchor="w", padx=40)
phone_entry = tk.Entry(root, width=40)
phone_entry.pack(pady=5)

# Buttons
submit_button = tk.Button(
    root,
    text="Register",
    font=("Arial", 10, "bold"),
    bg="#4CAF50",
    fg="white",
    width=20,
    command=register_attendee,
)
submit_button.pack(pady=10)

view_button = tk.Button(
    root,
    text="View Registered Data",
    font=("Arial", 10, "bold"),
    bg="#2196F3",
    fg="white",
    width=20,
    command=view_attendees,
)
view_button.pack(pady=5)

root.mainloop()