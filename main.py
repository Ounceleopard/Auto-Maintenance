# Auto Maintenance


import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import messagebox

# Function to save service history to a log file
def save_service_history():
    vehicle_type = vehicle_type_var.get()
    vehicle_name = vehicle_name_entry.get()
    service_type = service_type_entry.get()
    service_date = service_date_calendar.get()
    notes = notes_text.get("1.0", "end-1c").strip()  # Get text from the Text widget and remove leading/trailing whitespace
    
    # Check if the "Notes" section is empty
    if not notes:
        # Display an error message in the GUI
        messagebox.showerror("Error", "Please enter something in the 'Notes' section.")
        return  # Exit the function without saving

    # Create a filename based on the vehicle type (e.g., car.log, bike.log)
    filename = f"{vehicle_type.lower()}.log"
    
    # Format the service history entry
    service_entry = f"{vehicle_name}, {service_type}, {service_date}, {notes}"
    
    # Append the service entry to the log file
    with open(filename, 'a') as log_file:
        log_file.write(service_entry + '\n')
    
    # Clear input fields
    vehicle_name_entry.delete(0, tk.END)
    service_type_entry.delete(0, tk.END)
    service_date_calendar.set_date(datetime.now())
    notes_text.delete("1.0", tk.END)  # Clear the Text widget 0
    
    # Update the service history display immediately
    display_service_history(0)

# Function to display car service history
def display_car_service_history():
    display_service_history("car")

# Function to display bike service history
def display_bike_service_history():
    display_service_history("bike")

# Function to display service history
def display_service_history(vehicle_type=None):
    if not vehicle_type:
        vehicle_type = vehicle_type_var.get()
    
    filename = f"{vehicle_type.lower()}.log"
    
    try:
        with open(filename, 'r') as log_file:
            service_history = log_file.readlines()
            # Clear previous content
            if vehicle_type == "car":
                car_service_history_tree.delete(*car_service_history_tree.get_children())
            elif vehicle_type == "bike":
                bike_service_history_tree.delete(*bike_service_history_tree.get_children())
            for entry in service_history:
                entry_data = entry.strip().split(", ")
                if len(entry_data) == 4:  # Ensure there are enough elements in entry_data
                    if vehicle_type == "car":
                        car_service_history_tree.insert("", tk.END, values=(entry_data[0], entry_data[1], entry_data[2], entry_data[3]))
                    elif vehicle_type == "bike":
                        bike_service_history_tree.insert("", tk.END, values=(entry_data[0], entry_data[1], entry_data[2], entry_data[3]))
    except FileNotFoundError:
        pass


# Function to delete selected service history entries
def delete_selected_service_entries(vehicle_type):
    tree = car_service_history_tree if vehicle_type == "car" else bike_service_history_tree
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showinfo("Info", "No entries selected for deletion.")
        return

    # Confirm the deletion with the user
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected entries?")
    if not confirm:
        return

    filename = f"{vehicle_type.lower()}.log"
    with open(filename, 'r') as log_file:
        lines = log_file.readlines()

    # Remove selected entries from the list
    selected_indices = [tree.index(item) for item in selected_items]
    lines = [line for i, line in enumerate(lines) if i not in selected_indices]

    # Write the updated list back to the file
    with open(filename, 'w') as log_file:
        log_file.writelines(lines)

    # Clear the selection and refresh the display
    tree.selection_remove(selected_items)
    display_service_history(vehicle_type)


# Function to search for and display matching service history entries
def search_service_history():
    keyword = search_entry.get().lower()
    
    # Clear previous selection
    car_service_history_tree.selection_remove(car_service_history_tree.selection())
    bike_service_history_tree.selection_remove(bike_service_history_tree.selection())

    # Search and highlight entries for car service history
    for item in car_service_history_tree.get_children():
        values = car_service_history_tree.item(item, 'values')
        if any(keyword in value.lower() for value in values):
            car_service_history_tree.selection_add(item)

    # Search and highlight entries for bike service history
    for item in bike_service_history_tree.get_children():
        values = bike_service_history_tree.item(item, 'values')
        if any(keyword in value.lower() for value in values):
            bike_service_history_tree.selection_add(item)

    # Update the service history display
    display_service_history()

# Create the main window
app = tk.Tk()
app.title("Auto Maintenance")
app.geometry("1080x720") # Set initial window size (WxH)
app.config(bg="DarkBlue") # Setting background color of the window 

# Vehicle type selection
vehicle_type_var = tk.StringVar()
vehicle_type_var.set("Select")
vehicle_type_label = tk.Label(app, text="Type:")
vehicle_type_menu = tk.OptionMenu(app, vehicle_type_var, "Car", "Bike")
# Type button and menu
vehicle_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w") # Type text
vehicle_type_menu.grid(row=0, column=0, padx=10, pady=10) # Type menu


# Create labels and entry fields
vehicle_name_label = tk.Label(app, text="Name:")
vehicle_name_entry = tk.Entry(app, width=40)

service_type_label = tk.Label(app, text="Service Type:")
service_type_entry = tk.Entry(app)

service_date_label = tk.Label(app, text="Service Date:")
service_date_calendar = DateEntry(app, width=16, background="Grey", foreground="white", borderwidth=2)

notes_label = tk.Label(app, text="Notes:")
notes_text = tk.Text(app, height=5, width=30, wrap=tk.WORD)  # Adjust the height and width as needed, and set wrap=tk.WORD

# Create a button to save service history
save_button = tk.Button(app, text="Save Service History", command=save_service_history)

# Create delete buttons for car and bike service history
delete_car_button = tk.Button(app, text="Delete Selected (Car)", command=lambda: delete_selected_service_entries("car"))
delete_bike_button = tk.Button(app, text="Delete Selected (Bike)", command=lambda: delete_selected_service_entries("bike"))

# Grid layout for delete buttons
delete_car_button.grid(row=10, column=2, columnspan=2, pady=10)
delete_bike_button.grid(row=14, column=2, columnspan=2, pady=10)


# Create labels to display service history
car_service_history_label = tk.Label(app, text="Car Service History:")
bike_service_history_label = tk.Label(app, text="Bike Service History:")
car_service_history_label.grid(row=8, column=0, padx=10, pady=5, columnspan=2)
bike_service_history_label.grid(row=13, column=0, padx=10, pady=5, columnspan=2)

# Create Treeview widgets to display service history without "Type" column
car_service_history_tree = ttk.Treeview(app, columns=("Name", "Service", "Date", "Notes"), show="headings", selectmode='extended', height=7) # 7 box height
bike_service_history_tree = ttk.Treeview(app, columns=("Name", "Service", "Date", "Notes"), show="headings", selectmode='extended', height=7) # 7 box height (bottom of screen)

for tree in [car_service_history_tree, bike_service_history_tree]:
    tree.heading("Name", text="Name")
    tree.heading("Service", text="Service")
    tree.heading("Date", text="Date")
    tree.heading("Notes", text="Notes")
    
# Modify the Treeview widget rows and columns configuration
car_service_history_tree.grid(row=10, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")
bike_service_history_tree.grid(row=14, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

# Create a Text widget for displaying service history entries
service_history_text = tk.Text(app, height=8, width=40, wrap=tk.WORD)

# Create a search frame
search_frame = tk.Frame(app)
search_frame.grid(row=15, column=0, columnspan=2, padx=10, pady=5)

# Create a search field and button
search_label = tk.Label(search_frame, text="Search:")
search_entry = tk.Entry(search_frame)
search_button = tk.Button(search_frame, text="Search", command=search_service_history)  # Corrected placement of the command
search_hint_label = tk.Label(search_frame, text="(Name, Service, Date, or Notes)")
search_label.grid(row=0, column=0, padx=5, pady=5)
search_entry.grid(row=0, column=1, padx=5, pady=5)
search_hint_label.grid(row=0, column=2, padx=5, pady=5)
search_button.grid(row=0, column=3, padx=5, pady=5)

# Grid layout for labels and entry fields
vehicle_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
vehicle_name_entry.grid(row=1, column=0, padx=10, pady=5)
#service type
service_type_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
service_type_entry.grid(row=1, column=1, padx=10, pady=5)
# Service date
service_date_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
service_date_calendar.grid(row=0, column=1, padx=10, pady=5) # Calender 
#notes
notes_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
notes_text.grid(row=2, column=0, padx=10, pady=5) # Notes Box
# save button
save_button.grid(row=2, column=1, padx= 10, pady=10)

# Display initial service history
display_car_service_history()
display_bike_service_history()

# Start the main loop
app.mainloop()
