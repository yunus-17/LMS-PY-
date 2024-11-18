from tkinter import *
from tkinter import messagebox
import mysql.connector

# Function to handle the login process
def login_user():
    email = email_entry.get()
    password = password_entry.get()

    # Basic validation to check if fields are filled
    if not email or not password:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    # Database connection setup
    try:
        # Connect to MySQL Database
        connection = mysql.connector.connect(
            host="localhost",        # Database host
            user="root",             # Your MySQL username
            password="",             # Your MySQL password
            database="libpy" # Database name
        )

        cursor = connection.cursor()

        # Check if the user exists in the database with the given email and password
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()  # Fetch one record

        if user:
            messagebox.showinfo("Login Success", "Login successful!")
            # Here, you can redirect to another page or perform actions post-login.
            # For now, just close the login window.
            root.destroy()
        else:
            messagebox.showwarning("Login Error", "Invalid email or password!")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create the main window
root = Tk()
root.title("Login Page")
root.geometry("400x400")

# Login Form
form_frame = Frame(root, padx=20, pady=20)
form_frame.pack(padx=10, pady=10)

# Email Field
email_label = Label(form_frame, text="Email (Gmail):")
email_label.grid(row=0, column=0, sticky=W, pady=5)
email_entry = Entry(form_frame, width=30)
email_entry.grid(row=0, column=1, pady=5)

# Password Field
password_label = Label(form_frame, text="Password:")
password_label.grid(row=1, column=0, sticky=W, pady=5)
password_entry = Entry(form_frame, width=30, show="*")  # show="*" hides the password text
password_entry.grid(row=1, column=1, pady=5)

# Login Button
login_button = Button(root, text="Login", bg="#4CAF50", fg="white", command=login_user)
login_button.pack(pady=20)

# Signup Redirect Button
signup_button = Button(root, text="Don't have an account? Sign Up", bg="#f44336", fg="white", command=lambda: root.destroy())
signup_button.pack()

# Run the Tkinter event loop
root.mainloop()
