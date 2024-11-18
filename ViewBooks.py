from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql

# Database connection parameters
host = "localhost"  # Use localhost for XAMPP
user = "root"       # Default user for XAMPP
password = ""       # Leave blank if no password is set
database = "libpy"  # Your database name
port = 3306         # Default MySQL port

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

    # Test the connection
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    print(f"Connected to database: {db_name[0]}")

except pymysql.MySQLError as e:
    print(f"Error connecting to database: {e}")
    messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")

# Add Books functionality
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
    
    root.destroy()

def addBook():
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4, root
    
    root = Toplevel()
    root.title("Add Books")
    root.geometry("600x500")
    root.config(bg="#ff6e40")

    Canvas1 = Canvas(root, bg="#ff6e40")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Add Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.4)
        
    Label(labelFrame, text="Book ID: ", bg='black', fg='white').place(relx=0.05, relheight=0.08)
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, relwidth=0.62, relheight=0.08)
        
    Label(labelFrame, text="Title: ", bg='black', fg='white').place(relx=0.05, rely=0.2, relheight=0.08)
    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.08)
        
    Label(labelFrame, text="Author: ", bg='black', fg='white').place(relx=0.05, rely=0.4, relheight=0.08)
    bookInfo3 = Entry(labelFrame)
    bookInfo3.place(relx=0.3, rely=0.4, relwidth=0.62, relheight=0.08)
        
    Label(labelFrame, text="Status (Avail/Issued): ", bg='black', fg='white').place(relx=0.05, rely=0.6, relheight=0.08)
    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.3, rely=0.6, relwidth=0.62, relheight=0.08)
        
    Button(root, text="SUBMIT", bg='#d1ccc0', fg='black', command=bookRegister).place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)
    Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy).place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

# View Books functionality
def viewBooks():
    root = Toplevel()
    root.title("View Books")
    root.geometry("600x500")
    root.config(bg="#12a4d9")

    Canvas1 = Canvas(root, bg="#12a4d9")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    Label(labelFrame, text="%-10s%-40s%-30s%-20s" % ('BID', 'Title', 'Author', 'Status'), bg='black', fg='white').place(relx=0.07, rely=0.1)
    Label(labelFrame, text="----------------------------------------------------------------------------", bg='black', fg='white').place(relx=0.05, rely=0.2)

    getBooks = "SELECT * FROM {}".format(bookTable)
    try:
        cursor.execute(getBooks)
        connection.commit()
        y = 0.25
        for i in cursor.fetchall():
            Label(labelFrame, text="%-10s%-30s%-30s%-20s" % (i[0], i[1], i[2], i[3]), bg='black', fg='white').place(relx=0.07, rely=y)
            y += 0.1
    except pymysql.MySQLError as e:
        messagebox.showinfo("Failed to fetch records", f"Error: {e}")

    Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy).place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

# Main application
def mainApp():
    global root
    root = Tk()
    root.title("Library Management System")
    root.geometry("800x600")
    root.config(bg="#ff6e40")

    header = Frame(root, bg="#333", height=50)
    header.pack(side=TOP, fill=X)

    Button(header, text="Add Books", bg="#444", fg="white", font=("Arial", 12), command=addBook).pack(side=LEFT, padx=10, pady=5)
    Button(header, text="View Books", bg="#444", fg="white", font=("Arial", 12), command=viewBooks).pack(side=LEFT, padx=10, pady=5)

    main_frame = Frame(root, bg="#fff")
    main_frame.pack(fill=BOTH, expand=True)

    Label(main_frame, text="Welcome to the Library Management System", font=("Arial", 18), bg="#ff6e40", fg="#000").pack(pady=100)

    root.mainloop()

if connection:
    cursor.close()
    connection.close()

mainApp()
