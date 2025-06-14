import tkinter as tk
from tkinter import messagebox

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Application")
        self.root.geometry("600x700")
        self.root.configure(bg="#000000")  # Set background color to black
        self.contacts = {}
        self.load_contacts()
        
        title = tk.Label(root, text="Contact Book", font=("Helvetica", 24, "bold"), bg="#000000", fg="white")
        title.pack(pady=10)

        input_frame = tk.Frame(root, bg="#000000")
        input_frame.pack(pady=10)

        self.placeholders = {
            'name': "Name",
            'phone': "Phone",
            'email': "Email",
            'address': "Address"
        }

        self.name_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=15, fg="white", bg="#333333")
        self.name_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.name_entry, self.placeholders['name'])
        self.name_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['name']))
        self.name_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['name']))

        self.phone_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=15, fg="white", bg="#333333")
        self.phone_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.phone_entry, self.placeholders['phone'])
        self.phone_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['phone']))
        self.phone_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['phone']))

        self.email_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20, fg="white", bg="#333333")
        self.email_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.email_entry, self.placeholders['email'])
        self.email_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['email']))
        self.email_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['email']))

        self.address_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20, fg="white", bg="#333333")
        self.address_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.address_entry, self.placeholders['address'])
        self.address_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['address']))
        self.address_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['address']))

        add_btn = tk.Button(input_frame, text="Add Contact", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=self.add_contact)
        add_btn.pack(side=tk.LEFT, padx=8)

        clear_fields_btn = tk.Button(input_frame, text="Clear Fields", font=("Helvetica", 12, "bold"), bg="#FFC107", fg="black", command=self.clear_entries)
        clear_fields_btn.pack(side=tk.LEFT, padx=8)

        search_frame = tk.Frame(root, bg="#000000")
        search_frame.pack(pady=(10, 0), fill=tk.X, padx=10)
        search_label = tk.Label(search_frame, text="Search:", font=("Helvetica", 14), bg="#000000", fg="white")
        search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="#333333", fg="white")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_contacts)

        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, font=("Helvetica", 14), height=20, yscrollcommand=self.scrollbar.set, bg="#333333", fg="white")
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self.view_contact)
        self.scrollbar.config(command=self.listbox.yview)

        buttons_frame = tk.Frame(root, bg="#000000")
        buttons_frame.pack(pady=10)

        delete_btn = tk.Button(buttons_frame, text="Delete Contact", font=("Helvetica", 12, "bold"), bg="#f44336", fg="white", command=self.delete_contact)
        delete_btn.pack(side=tk.LEFT, padx=5)

        update_btn = tk.Button(buttons_frame, text="Update Contact", font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", command=self.update_contact)
        update_btn.pack(side=tk.LEFT, padx=5)

        view_btn = tk.Button(buttons_frame, text="View Contact", font=("Helvetica", 12, "bold"), bg="#8BC34A", fg="white", command=self.view_contact)
        view_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(buttons_frame, text="Clear All", font=("Helvetica", 12, "bold"), bg="#9E9E9E", fg="white", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=5)

        self.refresh_listbox()

    def set_placeholder(self, entry, placeholder):
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg="grey")

    def clear_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="white")

    def add_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        if name == "" or name == self.placeholders['name'] or phone == "" or phone == self.placeholders['phone']:
            messagebox.showwarning("Warning", "Name and Phone are required.")
            return

        self.contacts[name] = {
            'phone': phone,
            'email': email if email != self.placeholders['email'] else '',
            'address': address if address != self.placeholders['address'] else ''
        }
        self.clear_entries()
        self.save_contacts()
        self.refresh_listbox()

    def update_contact(self, event=None):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to update.")
            return
        index = selected[0]
        name = self.listbox.get(index).split(" - ")[0]
        contact = self.contacts[name]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.name_entry.config(fg="white")
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, contact['phone'])
        self.phone_entry.config(fg="white")
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contact['email'] if contact['email'] else self.placeholders['email'])
        self.email_entry.config(fg="white" if contact['email'] else "grey")
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, contact['address'] if contact['address'] else self.placeholders['address'])
        self.address_entry.config(fg="white" if contact['address'] else "grey")

    def delete_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return
        index = selected[0]
        name = self.listbox.get(index).split(" - ")[0]
        del self.contacts[name]
        self.save_contacts()
        self.refresh_listbox()
        self.clear_entries()

    def view_contact(self, event=None):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("View Contact", "Please select a contact to view.")
            return
        index = selected[0]
        name = self.listbox.get(index).split(" - ")[0]
        c = self.contacts[name]
        messagebox.showinfo("Contact Details", f"Name: {name}\nPhone: {c['phone']}\nEmail: {c['email']}\nAddress: {c['address']}")

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all contacts?"):
            self.contacts.clear()
            self.save_contacts()
            self.refresh_listbox()
            self.clear_entries()

    def filter_contacts(self, event=None):
        search_term = self.search_entry.get().strip().lower()
        self.listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            if search_term in name.lower() or search_term in details['phone']:
                self.listbox.insert(tk.END, f"{name} - {details['phone']}")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            self.listbox.insert(tk.END, f"{name} - {details['phone']}")

    def save_contacts(self):
        try:
            with open("contacts.txt", "w", encoding="utf-8") as f:
                for name, details in self.contacts.items():
                    email = details['email'].replace("|", "/") if details['email'] else ""
                    address = details['address'].replace("|", "/") if details['address'] else ""
                    f.write(f"{name}|{details['phone']}|{email}|{address}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {e}")

    def load_contacts(self):
        try:
            with open("contacts.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split("|")
                        if len(parts) == 4:
                            name, phone, email, address = parts
                            self.contacts[name] = {'phone': phone, 'email': email, 'address': address}
        except FileNotFoundError:
            pass

    def clear_entries(self):
        self.set_placeholder(self.name_entry, self.placeholders['name'])
        self.set_placeholder(self.phone_entry, self.placeholders['phone'])
        self.set_placeholder(self.email_entry, self.placeholders['email'])
        self.set_placeholder(self.address_entry, self.placeholders['address'])

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
