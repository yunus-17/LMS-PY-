from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

# Database connection parameters
host = "localhost"  # or "127.0.0.1"
user = "root"       # your MariaDB username
password = ""       # your MariaDB password
database = "libpy"  # your database name
port = 3306         # MariaDB default port

# Global variable for database connection and cursor
connection = None
cursor = None
bookTable = "books" 

# Connect to MariaDB
try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    print("Connection successful!")

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Example query to test the connection
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    print(f"Connected to database: {db_name[0]}")

except pymysql.MySQLError as e:
    print(f"Error connecting to database: {e}")
    messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")

# Enter Table Names here
issueTable = "books_issued"
bookTable = "books"  # Book Table

# Function to delete a book
def deleteBook():
    global connection, cursor
    
    bid = bookInfo1.get().strip()  # Ensure no extra spaces
    if not bid:
        messagebox.showerror("Error", "Please enter a valid Book ID.")
        return

    # Check if the book exists in the database
    try:
        cursor.execute("SELECT * FROM {} WHERE bid = %s".format(bookTable), (bid,))
        book = cursor.fetchone()
        
        if not book:
            messagebox.showinfo("Error", "Book ID not found in the database.")
            return

        # Delete from books_issued table first if the book has been issued
        cursor.execute("DELETE FROM {} WHERE bid = %s".format(issueTable), (bid,))

        # Now delete from the books table
        cursor.execute("DELETE FROM {} WHERE bid = %s".format(bookTable), (bid,))

        # Commit the changes
        connection.commit()
        
        messagebox.showinfo('Success', "Book Record Deleted Successfully")
        
        # Clear the input field
        bookInfo1.delete(0, END)
        
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to delete record: {e}")
    
    print(f"Deleted Book ID: {bid}")

# Function to open the GUI for book deletion
def delete(): 
    global bookInfo1, Canvas1, root
    
    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("600x500")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#006B38")
    Canvas1.pack(expand=True, fill=BOTH)
        
    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
        
    headingLabel = Label(headingFrame1, text="Delete Book", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)   
        
    # Book ID to Delete
    lb2 = Label(labelFrame, text="Book ID: ", bg='black', fg='white')
    lb2.place(relx=0.05, rely=0.5)
        
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.5, relwidth=0.62)
    
    # Submit Button
    SubmitBtn = Button(root, text="SUBMIT", bg='#d1ccc0', fg='black', command=deleteBook)
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)
    
    quitBtn = Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)
    
    root.mainloop()

# Call the delete function to start the GUI
delete()

# Close the connection when done
if connection:
    cursor.close()
    connection.close()
    print("Connection closed.")
