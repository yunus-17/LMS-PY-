from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql
from PIL import Image
import pymysql

def bookRegister():
    bid = bookInfo1.get()
    title = bookInfo2.get()
    author = bookInfo3.get()
    status = bookInfo4.get().lower()

    insertBooks = "INSERT INTO " + bookTable + " (book_id, title, author, status) VALUES (%s, %s, %s, %s)"
    
    try:
        cur.execute(insertBooks, (bid, title, author, status))
        con.commit()
        messagebox.showinfo('Success', "Book added successfully")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Can't add data into Database\nError: {e}")

        print(f"Book ID: {bid}, Title: {title}, Author: {author}, Status: {status}")
        # Only close the window if needed
        # root.destroy()

def addBook():
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4, Canvas1, con, cur, bookTable, root

    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("600x500")

    # Add your own database name and password here
    mypass = "root"
    mydatabase = "db"

    # Establish a connection to the database
    try:
        con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
        cur = con.cursor()
    except pymysql.Error as e:
        messagebox.showerror("Connection Error", f"Failed to connect to database\nError: {e}")
        return

    # Table name
    bookTable = "books"

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#ff6e40")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Add Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.4)

    # Book ID
    lb1 = Label(labelFrame, text="Book ID: ", bg='black', fg='white')
    lb1.place(relx=0.05, rely=0.2, relheight=0.08)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.08)

    # Title
    lb2 = Label(labelFrame, text="Title: ", bg='black', fg='white')
    lb2.place(relx=0.05, rely=0.35, relheight=0.08)

    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3, rely=0.35, relwidth=0.62, relheight=0.08)

    # Author
    lb3 = Label(labelFrame, text="Author: ", bg='black', fg='white')
    lb3.place(relx=0.05, rely=0.50, relheight=0.08)

    bookInfo3 = Entry(labelFrame)
    bookInfo3.place(relx=0.3, rely=0.50, relwidth=0.62, relheight=0.08)

    # Status
    lb4 = Label(labelFrame, text="Status (Avail/Issued): ", bg='black', fg='white')
    lb4.place(relx=0.05, rely=0.65, relheight=0.08)

    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.3, rely=0.65, relwidth=0.62, relheight=0.08)

    # Submit Button
    SubmitBtn = Button(root, text="SUBMIT", bg='#d1ccc0', fg='black', command=bookRegister)
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    # Quit Button
    quitBtn = Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()

addBook()