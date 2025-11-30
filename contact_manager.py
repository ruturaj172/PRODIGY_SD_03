import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os

class ContactManagerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Contact Manager")
        master.geometry("600x450") # Increased size for better layout

        self.contacts = [] # List to store contact dictionaries
        self.filename = "contacts.csv"
        self.load_contacts()

        # --- Frames for Better Layout ---
        self.frame_buttons = tk.Frame(master, bd=2, relief="groove")
        self.frame_buttons.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)

        self.frame_list = tk.Frame(master, bd=2, relief="groove")
        self.frame_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=5)

        # --- Buttons ---
        self.btn_add = tk.Button(self.frame_buttons, text="Add New Contact", command=self.add_contact)
        self.btn_add.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_edit = tk.Button(self.frame_buttons, text="Edit Contact", command=self.edit_contact)
        self.btn_edit.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_delete = tk.Button(self.frame_buttons, text="Delete Contact", command=self.delete_contact)
        self.btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_refresh = tk.Button(self.frame_buttons, text="Refresh List", command=self.update_contact_list_display)
        self.btn_refresh.pack(side=tk.LEFT, padx=5, pady=5)

        # --- Contact List Display (Listbox) ---
        self.contact_listbox = tk.Listbox(self.frame_list, selectmode=tk.SINGLE, height=15)
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.scrollbar = tk.Scrollbar(self.frame_list, orient="vertical", command=self.contact_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_listbox.config(yscrollcommand=self.scrollbar.set)

        self.update_contact_list_display() # Initial display

    def load_contacts(self):
        """Loads contacts from the CSV file into memory."""
        self.contacts = []
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.contacts.append(row)
        print(f"Loaded {len(self.contacts)} contacts.")

    def save_contacts(self):
        """Saves current contacts in memory to the CSV file."""
        if not self.contacts:
            # If no contacts, ensure file is empty or removed if it exists
            if os.path.exists(self.filename):
                os.remove(self.filename)
            return

        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            # Get fieldnames from the first contact's keys
            fieldnames = self.contacts[0].keys() if self.contacts else ['Name', 'Phone', 'Email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.contacts)
        print(f"Saved {len(self.contacts)} contacts.")


    def update_contact_list_display(self):
        """Clears and repopulates the Listbox with current contacts."""
        self.contact_listbox.delete(0, tk.END) # Clear existing items
        for i, contact in enumerate(self.contacts):
            display_text = f"{contact.get('Name', 'N/A')} - {contact.get('Phone', 'N/A')}"
            self.contact_listbox.insert(tk.END, display_text)

    def add_contact(self):
        """Opens a new window to add a contact."""
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Contact")
        add_window.geometry("300x200")

        labels = ["Name:", "Phone:", "Email:"]
        entries = {}

        for i, text in enumerate(labels):
            tk.Label(add_window, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(add_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[text[:-1]] = entry # Store entry widgets by name (e.g., 'Name', 'Phone')

        def save():
            name = entries['Name'].get().strip()
            phone = entries['Phone'].get().strip()
            email = entries['Email'].get().strip()

            if not name:
                messagebox.showerror("Error", "Name cannot be empty.", parent=add_window)
                return

            new_contact = {'Name': name, 'Phone': phone, 'Email': email}
            self.contacts.append(new_contact)
            self.save_contacts()
            self.update_contact_list_display()
            add_window.destroy()

        tk.Button(add_window, text="Save Contact", command=save).grid(row=len(labels), columnspan=2, pady=10)

    def edit_contact(self):
        """Opens a window to edit the selected contact."""
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a contact to edit.")
            return

        index_to_edit = selected_index[0]
        original_contact = self.contacts[index_to_edit]

        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Edit Contact: {original_contact.get('Name', '')}")
        edit_window.geometry("300x200")

        labels = ["Name:", "Phone:", "Email:"]
        entries = {}

        for i, text in enumerate(labels):
            tk.Label(edit_window, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            # Pre-fill with existing data
            key = text[:-1]
            entry.insert(0, original_contact.get(key, ''))
            entries[key] = entry

        def update():
            name = entries['Name'].get().strip()
            phone = entries['Phone'].get().strip()
            email = entries['Email'].get().strip()

            if not name:
                messagebox.showerror("Error", "Name cannot be empty.", parent=edit_window)
                return

            self.contacts[index_to_edit] = {'Name': name, 'Phone': phone, 'Email': email}
            self.save_contacts()
            self.update_contact_list_display()
            edit_window.destroy()

        tk.Button(edit_window, text="Update Contact", command=update).grid(row=len(labels), columnspan=2, pady=10)


    def delete_contact(self):
        """Deletes the selected contact."""
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return

        index_to_delete = selected_index[0]
        contact_name = self.contacts[index_to_delete].get('Name', 'Unknown')

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {contact_name}?", icon='warning'):
            del self.contacts[index_to_to_delete]
            self.save_contacts()
            self.update_contact_list_display()
            messagebox.showinfo("Success", f"{contact_name} deleted.")


# --- Main program execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerGUI(root)
    root.mainloop()