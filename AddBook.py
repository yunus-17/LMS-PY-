from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

# Database connection parameters
host = "localhost"  # Use localhost for XAMPP
user = "root"       # Default user for XAMPP
password = ""       # Leave blank if no password is set
database = "libpy"  # Your database name
port = 3306         # Default MySQL port

# Global variables
connection = None
cursor = None
bookTable = "books"  # Define your table name

# Connect to the MySQL database
try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    print("Connection successful!")

    # Create a cursor object
    cursor = connection.cursor()

    # Example query to test the connection
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    print(f"Connected to database: {db_name[0]}")

except pymysql.MySQLError as e:
    print(f"Error connecting to database: {e}")
    messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")


def bookRegister():
    global connection
    bid = bookInfo1.get()
    title = bookInfo2.get()
    author = bookInfo3.get()
    status = bookInfo4.get().lower()
    
    insertBooks = "INSERT INTO {} (bid, title, author, status) VALUES (%s, %s, %s, %s)".format(bookTable)

    try:
        cursor.execute(insertBooks, (bid, title, author, status))
        connection.commit()
        messagebox.showinfo('Success', "Book added successfully")
    except Exception as e:
        messagebox.showinfo("Error", f"Can't add data into Database: {e}")
    
    print(bid, title, author, status)
    root.destroy()


# Function to add a book (GUI setup)
def addBook():
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4, Canvas1, root

    root = Tk()
    root.title("Library Management System")
    root.minsize(width=400, height=400)
    root.geometry("800x600")

    # Navigation bar
    def create_nav_bar():
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        nav_menu = Menu(menu_bar, tearoff=0)
        nav_menu.add_command(label="Add Books", command=addBook)
        nav_menu.add_command(label="View Books")
        nav_menu.add_command(label="Delete Books")
        nav_menu.add_command(label="Login")
        nav_menu.add_command(label="Signup")

        menu_bar.add_cascade(label="Navigation", menu=nav_menu)

    create_nav_bar()

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#ff6e40")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Add Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Book ID
    lb1 = Label(labelFrame, text="Book ID: ", bg='black', fg='white')
    lb1.place(relx=0.05, relheight=0.08)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, relwidth=0.62, relheight=0.08)

    # Title
    lb2 = Label(labelFrame, text="Title: ", bg='black', fg='white')
    lb2.place(relx=0.05, rely=0.2, relheight=0.08)

    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.08)

    # Book Author
    lb3 = Label(labelFrame, text="Author: ", bg='black', fg='white')
    lb3.place(relx=0.05, rely=0.4, relheight=0.08)

    bookInfo3 = Entry(labelFrame)
    bookInfo3.place(relx=0.3, rely=0.4, relwidth=0.62, relheight=0.08)

    # Book Status
    lb4 = Label(labelFrame, text="Status (Avail/Issued): ", bg='black', fg='white')
    lb4.place(relx=0.05, rely=0.6, relheight=0.08)

    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.3, rely=0.6, relwidth=0.62, relheight=0.08)

    # Submit Button
    SubmitBtn = Button(root, text="SUBMIT", bg='#d1ccc0', fg='black', command=bookRegister)
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()


# Call the addBook function to start the GUI
addBook()

# Close the connection when done
if connection:
    cursor.close()
    connection.close()
    print("Connection closed.")
