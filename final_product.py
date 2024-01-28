# Example Contact Manager with Tkinter

# Importing necessary modules from the tkinter library
import tkinter as tk
import tkinter.messagebox as mb
import csv
import os

# Constants for file handling
FILENAME = "contacts.csv"
FIELDS = ["Name", "Phone", "Email"]

# Class for the contact form window
class ContactForm(tk.Toplevel):

    # Constructor method
    def __init__(self, master, mode, contact=None):

        # Initializing the Toplevel window
        super().__init__(master)
        self.master = master
        self.mode = mode
        self.contact = contact
        self.title(f"{mode} Contact")
        self.resizable(False, False)
        self.grab_set()

        # Creating a frame for the form
        self.form_frame = tk.Frame(self, padx=10, pady=10)
        self.form_frame.pack()

        # Creating labels and entry widgets for name, email, and phone
        self.name_label = tk.Label(self.form_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1)

        self.email_label = tk.Label(self.form_frame, text="Email:")
        self.email_label.grid(row=1, column=0, sticky="w")
        self.email_entry = tk.Entry(self.form_frame)
        self.email_entry.grid(row=1, column=1)

        self.phone_label = tk.Label(self.form_frame, text="Phone:")
        self.phone_label.grid(row=2, column=0, sticky="w")
        self.phone_entry = tk.Entry(self.form_frame)
        self.phone_entry.grid(row=2, column=1)

        # Creating a submit button with a callback to submit_form method
        self.submit_button = tk.Button(self.form_frame, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=3, columnspan=2, pady=10)

        # If in update mode, pre-fill the form with existing contact information
        if self.mode == "Update":
            self.name_entry.insert(0, self.contact["Name"])
            self.email_entry.insert(0, self.contact["Email"])
            self.phone_entry.insert(0, self.contact["Phone"])

    # Method to handle form submission
    def submit_form(self):

        # Retrieving data from the entry widgets
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        # Validating that all fields are filled
        if not name or not email or not phone:
            mb.showerror("Error", "Please fill all the fields")
            return

        # Displaying submitted information
        message = f"Name: {name}\nEmail: {email}\nPhone: {phone}"
        mb.showinfo("Submitted Information", message)

        # Updating contacts list based on the mode (Add or Update)
        if self.mode == "Add":
            self.master.contacts.append({"Name": name, "Email": email, "Phone": phone})
        elif self.mode == "Update" and self.contact:
            self.contact["Name"] = name
            self.contact["Email"] = email
            self.contact["Phone"] = phone

        # Writing updated contacts to the file, refreshing the list, and closing the form
        self.master.write_contacts()
        self.master.refresh_list()
        self.destroy()


# Class for the main contact list window
class ContactList(tk.Frame):

    # Constructor method
    def __init__(self, master):

        # Initializing the Frame
        super().__init__(master)
        self.master = master
        self.pack()

        # Creating a title label
        self.title_label = tk.Label(self, text="Contact Manager", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Creating a frame for the contact list
        self.list_frame = tk.Frame(self)
        self.list_frame.pack()

        # Creating a scrollbar and a listbox to display contacts
        self.scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.list_frame, width=40, height=15, yscrollcommand=self.scrollbar.set)

        # Configuring scrollbar and packing listbox and scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # Creating a frame for buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        # Creating buttons for Add, Update, Delete, and Exit operations
        self.add_button = tk.Button(self.button_frame, text="Add", width=12, command=self.add_contact)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Update", width=12, command=self.update_contact)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", width=12, command=self.delete_contact)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.exit_button = tk.Button(self, text="Exit", width=12, command=self.exit_program)
        self.exit_button.pack(pady=10)

        # Reading contacts from the file and initializing the contact list
        self.contacts = self.read_contacts()
        self.refresh_list()

    # Method to read contacts from the file
    def read_contacts(self):

        contacts = []
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as file:
                reader = csv.DictReader(file, fieldnames=FIELDS)
                for row in reader:
                    contacts.append(row)
        return contacts

    # Method to write contacts to the file
    def write_contacts(self):

        with open(FILENAME, "w") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writerows(self.contacts)

    # Method to refresh the contact list in the GUI
    def refresh_list(self):

        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox.insert(tk.END, f"{contact['Name']} - {contact['Phone']} - {contact['Email']}")

    # Method to open the contact form for adding a new contact
    def add_contact(self):

        ContactForm(self, "Add")

    # Method to open the contact form for updating an existing contact
    def update_contact(self):

        # Getting the selected contact index from the listbox
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            contact = self.contacts[index]
            ContactForm(self, "Update", contact)
        else:
            mb.showerror("Error", "Please select a contact to update")

    # Method to delete the selected contact
    def delete_contact(self):

        # Getting the selected contact index from the listbox
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            contact = self.contacts.pop(index)
            # Writing updated contacts to the file, refreshing the list, and showing a deletion message
            self.write_contacts()
            self.refresh_list()
            mb.showinfo("Deleted Contact", f"{contact['Name']} was deleted.")
        else:
            mb.showerror("Error", "Please select a contact to delete")

    # Method to exit the program
    def exit_program(self):

        self.master.destroy()


# Main function to run the application
def main():

    # Creating the main tkinter window
    root = tk.Tk()
    root.title("Contact Manager")
    root.resizable(False, False)

    # Creating and running the ContactList instance
    ContactList(root)
    root.mainloop()


# Entry point for the script
if __name__ == "__main__":
    main()
