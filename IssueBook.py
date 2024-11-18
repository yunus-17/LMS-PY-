from tkinter import *
from tkinter import messagebox
import pymysql

# Connect to MariaDB
host = "localhost"  # or "127.0.0.1"
user = "root"       # your MariaDB username
password = ""   # your MariaDB password
database = "libpy"  # your database name
port = 3306         # MariaDB default port

# Create a database connection
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
issueTable = "books_issued"
bookTable = "books"

def issue():
    global connection, cursor, allBid, root, inf1, inf2

    bid = inf1.get().strip()  # Strip any leading/trailing spaces from the input
    issueto = inf2.get()

    # Clear entries after button click
    inf1.delete(0, END)
    inf2.delete(0, END)

    # Check if the book ID exists
    try:
        cursor.execute("SELECT bid FROM {}".format(bookTable))
        allBid = [row[0] for row in cursor.fetchall()]
        print(f"All Book IDs: {allBid}")  # Debugging line

        if bid in allBid:
            cursor.execute("SELECT status FROM {} WHERE bid = %s".format(bookTable), (bid,))
            status = cursor.fetchone()

            if status[0] == 'avail':
                # Proceed to issue the book
                cursor.execute("INSERT INTO {} (bid, issued_to) VALUES (%s, %s)".format(issueTable), (bid, issueto))
                cursor.execute("UPDATE {} SET status = 'issued' WHERE bid = %s".format(bookTable), (bid,))
                connection.commit()
                messagebox.showinfo('Success', "Book Issued Successfully")
                root.destroy()
            else:
                messagebox.showinfo('Message', "Book Already Issued")
                return
        else:
            messagebox.showinfo("Error", "Book ID not present")
            return

    except pymysql.MySQLError as e:
        messagebox.showinfo("Error", f"Database error: {e}")

def issueBook():
    global issueBtn, labelFrame, inf1, inf2, quitBtn, root

    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("600x500")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#D6ED17")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Issue Book", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Book ID
    lb1 = Label(labelFrame, text="Book ID : ", bg='black', fg='white')
    lb1.place(relx=0.05, rely=0.2)

    inf1 = Entry(labelFrame)
    inf1.place(relx=0.3, rely=0.2, relwidth=0.62)

    # Issued To Student name
    lb2 = Label(labelFrame, text="Issued To : ", bg='black', fg='white')
    lb2.place(relx=0.05, rely=0.4)

    inf2 = Entry(labelFrame)
    inf2.place(relx=0.3, rely=0.4, relwidth=0.62)

    # Issue Button
    issueBtn = Button(root, text="Issue", bg='#d1ccc0', fg='black', command=issue)
    issueBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="Quit", bg='#aaa69d', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()

# Call the function to open the issue book window
issueBook()

# Close the connection when done
if connection:
    cursor.close()
    connection.close()
    print("Connection closed.")
