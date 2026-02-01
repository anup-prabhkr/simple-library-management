import customtkinter as ctk # type: ignore
from datetime import datetime, timedelta
from tkinter import ttk, messagebox
import json
import os

# Set the appearance and color theme for CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LibraryManagementSystem:
    def __init__(self, window):
        self.window = window
        self.window.title("Library Management System")
        self.window.geometry("1350x590")
        self.books = {}  # Store book info
        self.users = {}  # Store user info (name, unique ID, contact number, and books issued)
        self.registered_users = []  # Track registered users as tuples (name, unique_id, contact_number)

        # Title Label with modern font and color
        self.header = ctk.CTkLabel(window, text="Library Management System", font=("Bahnschrift", 36, "bold"))
        self.header.grid(row=0, column=0, columnspan=4, pady=12, sticky="nsew")

        # Create a frame to contain the book entry fields and buttons
        self.frame_entry = ctk.CTkFrame(window)
        self.frame_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
      
        # Add an empty row for spacing
        self.empty_row = ctk.CTkLabel(self.frame_entry, text="", height= 1)  # You can also use a CTkLabel or CTkFrame
        self.empty_row.grid(row=1)  # Span across two columns to center

        # Book Entry Fields
        self.label_book_title = ctk.CTkLabel(self.frame_entry, text="Book Title:", font=("Bahnschrift", 14))
        self.label_book_title.grid(row=2, column=0, padx=10, pady=2, sticky="e")
        self.entry_book_title = ctk.CTkEntry(self.frame_entry, font=("Bahnschrift", 14), width=220)
        self.entry_book_title.grid(row=2, column=1, padx=10, pady=2, sticky="ew")

        self.label_author = ctk.CTkLabel(self.frame_entry, text="Author:", font=("Bahnschrift", 14))
        self.label_author.grid(row=3, column=0, padx=10, pady=2, sticky="e")
        self.entry_author = ctk.CTkEntry(self.frame_entry, font=("Bahnschrift", 14))
        self.entry_author.grid(row=3, column=1, padx=10, pady=2, sticky="ew")

        self.label_quantity = ctk.CTkLabel(self.frame_entry, text="Quantity:", font=("Bahnschrift", 14))
        self.label_quantity.grid(row=4, column=0, padx=10, pady=2, sticky="e")
        self.entry_quantity = ctk.CTkEntry(self.frame_entry, font=("Bahnschrift", 14))
        self.entry_quantity.grid(row=4, column=1, padx=10, pady=2, sticky="ew")

        # Buttons with styling
        self.button_add_book = ctk.CTkButton(self.frame_entry, text="Add Book", command=self.add_book)
        self.button_add_book.grid(row=5, column=0, pady=20, padx=20, sticky="ew")

        self.button_remove_book = ctk.CTkButton(self.frame_entry, text="Remove Book", command=self.remove_book)
        self.button_remove_book.grid(row=5, column=1, pady=20, padx=30, sticky="ew")

        self.label_user = ctk.CTkLabel(self.frame_entry, text="User Name:", font=("Bahnschrift", 14))
        self.label_user.grid(row=6, column=0, padx=10, pady=3, sticky="e")
        self.entry_user = ctk.CTkEntry(self.frame_entry, font=("Bahnschrift", 14))
        self.entry_user.grid(row=6, column=1, padx=10, pady=3, sticky="ew")

        # User ID and Contact Fields
        self.label_user_id = ctk.CTkLabel(self.frame_entry, text="User ID:", font=("Bahnschrift", 14))
        self.label_user_id.grid(row=7, column=0, padx=10, pady=3, sticky="e")
        self.entry_user_id = ctk.CTkEntry(self.frame_entry, font=("Bahnschrift", 14))
        self.entry_user_id.grid(row=7, column=1, padx=10, pady=3, sticky="ew")

        self.label_contact_number = ctk.CTkLabel(self.frame_entry, text="Contact Number:", font=("Bahnschrift", 14))
        self.label_contact_number.grid(row=8, column=0, padx=10, pady=3, sticky="e")
        self.entry_contact_number = ctk.CTkEntry(self.frame_entry, font=("Bahnschrift", 14))
        self.entry_contact_number.grid(row=8, column=1, padx=10, pady=3, sticky="ew")

        # Add an empty row for spacing
        self.empty_row = ctk.CTkLabel(self.frame_entry, text="", height=10)  # You can also use a CTkLabel or CTkFrame
        self.empty_row.grid(row=9)  # Span across two columns to center

        # Buttons for user actions
        self.button_register_user = ctk.CTkButton(self.frame_entry, text="Register User", command=self.register_user)
        self.button_register_user.grid(row=10, column=0, pady=5, padx=20, sticky="ew")

        self.button_display_users = ctk.CTkButton(self.frame_entry, text="Show Registered Users", command=self.display_users)
        self.button_display_users.grid(row=10, column=1, pady=5, padx=30, sticky="ew")

        self.button_remove_user = ctk.CTkButton(self.frame_entry, text="Remove User", command=self.remove_user)
        self.button_remove_user.grid(row=11, column=0, pady=5, padx=20, sticky="ew")

        self.button_user_info = ctk.CTkButton(self.frame_entry, text="User Info", command=self.show_user_info)
        self.button_user_info.grid(row=11, column=1, pady=5, padx=30, sticky="ew")

        # Add a label and entry for the Issue Date
        self.label_issue_date = ctk.CTkLabel(self.frame_entry, text="Issue Date (YYYY-MM-DD):", font=("Bahnschrift", 14))
        self.label_issue_date.grid(row=12, column=0, padx=10, pady=2, sticky="e")
        self.entry_issue_date = ctk.CTkEntry(self.frame_entry, font=("Bahnschrift", 14))
        self.entry_issue_date.grid(row=12, column=1, padx=10, pady=12, sticky="ew")

        self.button_issue_book = ctk.CTkButton(self.frame_entry, text="Issue Book", command=self.issue_book)
        self.button_issue_book.grid(row=13, column=0, pady=5, padx=20, sticky="ew")

        self.button_return_book = ctk.CTkButton(self.frame_entry, text="Return Book", command=self.return_book)
        self.button_return_book.grid(row=13, column=1, pady=5, padx=30, sticky="ew")

        self.button_issue_detail = ctk.CTkButton(self.frame_entry, text="Issue Detail", command=self.issue_detail, width= 120)
        self.button_issue_detail.grid(row=14, column=0, columnspan=2, pady=8, padx=10)

        self.button_reset = ctk.CTkButton(self.frame_entry, text="Reset", command=self.reset, width = 10)
        self.button_reset.grid(row=14, column=1, pady=8)

        # Frame to hold the Treeview for consistent styling
        self.table_frame = ctk.CTkFrame(window)
        self.table_frame.grid(row=1, column=2, rowspan=30, columnspan=3, padx=(10, 20), sticky="nsew")

        self.table = ttk.Treeview(self.table_frame, columns=("Title", "Author", "Quantity", "Available", "Issued"), show='headings')
        self.table.pack(fill="both", expand=True)  # Fill the CTkFrame
        
        # Update column headers
        for col in ("Title", "Author", "Quantity", "Available", "Issued"):
            self.table.heading(col, text=col)
            if col == "Title":
                self.table.column(col, anchor="center", width=400)
            elif col == "Author":
                self.table.column(col, anchor="center")
            else:
                self.table.column(col, anchor="center", width=50)

        # Configure treeview style for dark mode
        style = ttk.Style()
        style.theme_use("default")  # Continue using ttk style while integrating into CustomTkinter
        style.configure("Treeview", background="#1C1E22", fieldbackground="#1C1E22", foreground="#FFFFFF", font=("Bahnschrift", 15), rowheight=35)
        style.configure("Treeview.Heading", background="#2463AA", font=("Bahnschrift", 16, "bold"))

        # Expandable Treeview grid
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(15, weight=1)

        # Load books and users from file
        self.load_data()

    def add_book(self):
        book_title = self.entry_book_title.get()
        author = self.entry_author.get()
        quantity = self.entry_quantity.get()

        if not book_title or not author or not quantity:
            messagebox.showerror("Book Entry Error", "Please fill out all book details.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Book Entry Error", "Quantity must be a number.")
            return

        if book_title in self.books:
            messagebox.showerror("Book Error", "This book already exists in the library.")
            return

        # Ensure both quantity and available fields are initialized correctly
        self.books[book_title] = {"author": author, "quantity": quantity, "available": quantity}
        self.update_table()
        messagebox.showinfo("Book Added", f"Book '{book_title}' by {author} added to the library.")
        self.save_data()
        self.reset()

    def remove_book(self):
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showinfo("Remove Book", "Please select a book to remove.")
            return

        item_values = self.table.item(selected_item)['values']
        book_title = item_values[0]

        del self.books[book_title]
        self.update_table()
        messagebox.showinfo("Remove Book", f"Book '{book_title}' removed from the library.")
        self.save_data()

    def register_user(self):
        """Register a new user with name, unique ID, and contact number."""
        user_name = self.entry_user.get()
        user_id = self.entry_user_id.get()
        contact_number = self.entry_contact_number.get()

        if not user_name or not user_id or not contact_number:
            messagebox.showerror("User Registration", "Please enter all details (Name, ID, Contact Number).")
            return

        for user in self.registered_users:
            if user_id == user[1]:
                messagebox.showerror("User Registration", f"User ID '{user_id}' is already registered.")
                return

        self.registered_users.append((user_name, user_id, contact_number))
        messagebox.showinfo("User Registration", f"User '{user_name}' registered successfully with ID: {user_id} and Contact: {contact_number}.")
        self.save_data()

    def display_users(self):
        """Display all registered users (name, ID, contact number)."""
        if self.registered_users:
            users_list = "\n".join([f"{user[0]}, ID: {user[1]}, Contact: {user[2]}" for user in self.registered_users])
            messagebox.showinfo("Registered Users", f"List of registered users:\n\n{users_list}")
        else:
            messagebox.showinfo("Registered Users", "No users are registered yet.")

    def remove_user(self):
        """Remove a registered user by name and ID."""
        user_name = self.entry_user.get()
        user_id = self.entry_user_id.get()

        if not user_name or not user_id:
            messagebox.showerror("Remove User", "Please enter both user name and user ID.")
            return

        # Find the user in registered_users
        user_to_remove = next((user for user in self.registered_users if user[0] == user_name and user[1] == user_id), None)

        if user_to_remove:
            self.registered_users.remove(user_to_remove)
            if user_name in self.users:
                del self.users[user_name]  # Remove user from issued books if exists
            messagebox.showinfo("Remove User", f"User '{user_name}' removed successfully.")
            self.save_data()
        else:
            messagebox.showerror("Remove User", f"User '{user_name}' with ID '{user_id}' not found.")

    def show_user_info(self):
        user_id = self.entry_user_id.get()  # Get user ID from entry

        if not user_id:
            messagebox.showerror("User Info", "Please enter the user's ID.")
            return

        # Find the user by their ID
        for user_name, user_data in self.users.items():
            if user_data["id"] == user_id:
                issued_books_info = "\n".join([f"{book['title']}, Issued: {book['issue_date']}, Return: {book['return_date']}" for book in user_data["issued_books"]])
                messagebox.showinfo("User Info", f"User: {user_name}, ID: {user_id},\n\nIssued Books:\n{issued_books_info}")
                return

        messagebox.showinfo("User Info", f"No books issued by a user with ID {user_id}.")

    def save_data(self):
        """Save books, users, and registered users to a JSON file."""
        data = {"books": self.books, "users": self.users, "registered_users": self.registered_users}
        with open("book1.json", "w") as file:
            json.dump(data, file)

    def issue_book(self):
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showinfo("Issue Error", "Please select a book to issue.")
            return

        item_values = self.table.item(selected_item)['values']
        user_name = self.entry_user.get()
        user_id = self.entry_user_id.get()
        issue_date_str = self.entry_issue_date.get()

        # Validate the issue date
        try:
            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Date Error", "Invalid issue date format. Use YYYY-MM-DD.")
            return

        if not user_name or not user_id:
            messagebox.showinfo("User Error", "Please enter your name and ID.")
            return

        # Check if the user is registered
        registered_user = next((user for user in self.registered_users if user[0] == user_name and user[1] == user_id), None)
        if not registered_user:
            messagebox.showinfo("User Error", f"User '{user_name}' with ID '{user_id}' is not registered.")
            return

        book_title = item_values[0]

        # Check if the book exists and is available
        if self.books.get(book_title, {}).get("available", 0) > 0:
            # Check if the user has already issued this specific book
            if user_name in self.users:
                issued_books = self.users[user_name]["issued_books"]
                # Check if the book has already been issued to this user
                if any(book["title"] == book_title for book in issued_books):
                    messagebox.showinfo("Issue Error", f"User '{user_name}' has already issued the book '{book_title}'.")
                    return

            # Reduce the available count of the book by 1
            self.books[book_title]["available"] -= 1

            # Calculate the return date (15 days from issue date)
            return_date = issue_date + timedelta(days=15)

            # Track which user has which books, along with issue and return dates
            issued_book_info = {"title": book_title,"issue_date": issue_date_str,"return_date": return_date.strftime('%Y-%m-%d')}

            # If the user has already issued other books, add this book to the issued list
            if user_name in self.users:
                self.users[user_name]["issued_books"].append(issued_book_info)
            else:
                # If this is the user's first issued book, create an entry for the user
                self.users[user_name] = {"id": user_id,"issued_books": [issued_book_info]}

            self.update_table()
            messagebox.showinfo("Book Issued", f"Book '{book_title}' has been issued to '{user_name}' with return date: {return_date.strftime('%Y-%m-%d')}.")
            self.save_data()
        else:
            messagebox.showinfo("Issue Error", "No copies of the selected book are currently available.")


    def return_book(self):
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showinfo("Return Error", "Please select a book to return.")
            return

        item_values = self.table.item(selected_item)['values']
        user_name = self.entry_user.get()
        book_title = item_values[0]

        if not user_name:
            messagebox.showinfo("User Error", "Please enter your name.")
            return

        # Ensure the user exists and the book is issued to them
        if user_name in self.users:
            issued_books = self.users[user_name]["issued_books"]
            for book in issued_books:
                if book["title"] == book_title:
                    issued_books.remove(book)
                    self.books[book_title]["available"] += 1
                    self.update_table()
                    messagebox.showinfo("Book Returned", f"Book '{book_title}' has been returned by '{user_name}'.")
                    self.save_data()
                    return

        messagebox.showinfo("Return Error", f"Book '{book_title}' is not issued to '{user_name}'.")

    def issue_detail(self):
        """Display all records of issued books along with the users who issued them and available quantity."""
        issued_books_info = []

        # Iterate through all users and their issued books
        for user_name, user_data in self.users.items():
            for book in user_data["issued_books"]:
                title = book["title"]
                issue_date = book.get("issue_date", "Unknown")
                return_date = book.get("return_date", "Unknown")

                # Get the available quantity from the books dictionary
                available_quantity = self.books.get(title, {}).get("available", "Unknown")

                # Format the details including available quantity and append to the list
                issued_books_info.append(f"Book Title: {title}\n"
                                        f"Issued by: {user_name}\n"
                                        f"Issue Date: {issue_date}, Return Date: {return_date}\n"
                                        f"Available Quantity: {available_quantity}\n")

        # If no books have been issued, display an appropriate message
        if not issued_books_info:
            messagebox.showinfo("Issued Books", "No books have been issued yet.")
        else:
            # Join all the issued book details and display in a messagebox
            issued_books_details = "\n".join(issued_books_info)
            messagebox.showinfo("Issued Books", issued_books_details)
    
    def load_data(self):
        """Load books, users, and registered users from a JSON file."""
        if os.path.exists("book1.json"):
            with open("book1.json", "r") as file:
                try:
                    data = json.load(file)
                    self.books = data.get("books", {})
                    self.users = data.get("users", {})
                    self.registered_users = data.get("registered_users", [])

                    # Ensure each book has the necessary fields
                    for book in self.books.values():
                        if "available" not in book:
                            book["available"] = book.get("quantity", 0)  # Default to quantity if 'available' is missing

                    self.update_table()
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Failed to load data from file.")
        
    def update_table(self):
        """Update the Treeview with current book data."""
        # Clear existing data
        for item in self.table.get_children():
            self.table.delete(item)

        # Insert updated data into the Treeview
        for title, book_info in self.books.items():
            author = book_info.get("author", "Unknown")
            quantity = book_info.get("quantity", 0)
            available = book_info.get("available", 0)
            
            # Calculate issued books
            issued_count = sum(1 for user in self.users.values() for book in user["issued_books"] if book["title"] == title)

            # Insert new row with issued count
            self.table.insert("", "end", values=(title, author, quantity, available, issued_count))

    def reset(self):
        """Clear all entry fields and deselect any selected rows in the table."""
        # Clear entry fields
        self.entry_book_title.delete(0, ctk.END)
        self.entry_author.delete(0, ctk.END)
        self.entry_quantity.delete(0, ctk.END)
        self.entry_user.delete(0, ctk.END)
        self.entry_user_id.delete(0, ctk.END)
        self.entry_contact_number.delete(0, ctk.END)
        self.entry_issue_date.delete(0, ctk.END)
        # Deselect selected rows in the table
        selected_items = self.table.selection()
        for item in selected_items:
            self.table.selection_remove(item)

# Run the program
if __name__ == "__main__":
    root = ctk.CTk()
    app = LibraryManagementSystem(root)
    root.mainloop()
    

