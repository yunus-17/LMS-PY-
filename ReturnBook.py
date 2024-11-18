from tkinter import *
from tkinter import messagebox
import pymysql

# Database connection parameters
host = "localhost"  # or "127.0.0.1"
user = "root"       # your MariaDB username
password = ""   # your MariaDB password
database = "libpy"  # your database name
port = 3306

# MariaDB default port
connection = None
cursor = None
bookTable = "books"  # Define your table name
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
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    print(f"Database version: {version[0]}")

except pymysql.MySQLError as e:
    print(f"Error connecting to database: {e}")

# Enter Table Names here
issueTable = "books_issued"  # Issue Table
bookTable = "books"  # Book Table

def return_book(bookInfo1):
    bid = bookInfo1.get()
    
    # Fetch all Book IDs from the issued table
    try:
        extractBid = "SELECT bid FROM {}".format(issueTable)
        cursor.execute(extractBid)
        allBid = [row[0] for row in cursor.fetchall()]  # List comprehension to create the list of Book IDs
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error fetching book IDs: {e}")
        return

    if bid in allBid:
        try:
            checkAvail = "SELECT status FROM {} WHERE bid = %s".format(bookTable)
            cursor.execute(checkAvail, (bid,))
            check = cursor.fetchone()

            if check and check[0] == 'issued':
                # If the book is issued, delete from issued table and update status
                issueSql = "DELETE FROM {} WHERE bid = %s".format(issueTable)
                updateStatus = "UPDATE {} SET status = 'avail' WHERE bid = %s".format(bookTable)
                cursor.execute(issueSql, (bid,))
                cursor.execute(updateStatus, (bid,))
                connection.commit()
                messagebox.showinfo('Success', "Book Returned Successfully")
            else:
                messagebox.showinfo('Message', "Book is already returned or not found.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error updating database: {e}")
    else:
        messagebox.showinfo("Error", "Book ID not present.")

    bookInfo1.delete(0, END)  # Clear the input field

def return_book_window(): 
    global bookInfo1, root

    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("600x500")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#006B38")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Return Book", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)   

    lb1 = Label(labelFrame, text="Book ID: ", bg='black', fg='white')
    lb1.place(relx=0.05, rely=0.5)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.5, relwidth=0.62)

    # Submit Button
    SubmitBtn = Button(root, text="Return", bg='#d1ccc0', fg='black', command=lambda: return_book(bookInfo1))
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()

# Call the function to open the return book window
return_book_window()

# Close the connection when done (only after the Tkinter event loop ends)
if connection:
    cursor.close()
    connection.close()
    print("Connection closed.")
