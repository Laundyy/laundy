import sqlite3

#Connect to a database.
db = sqlite3.connect("bookstore.db")

#Connect cursor object.
cur = db.cursor()

##cur.execute("DROP TABLE CLERK ")


#Define table.
table = """ CREATE TABLE CLERK (
        ID INT PRIMARY KEY NOT NULL,
        TITLE VARCHAR(15) NOT NULL,
        AUTHOR  CHAR(6) NOT NULL,
        QTY  INT NOT NULL
);"""


#Create vars to store ID's.
id1 = 3001; id2 = 3002; id3 = 3003; id4 = 3004; id5 = 3005
#Create vars to store titles.
tit1 = "A Tale of Two Cities" ; tit2 = "Harry Potter and the Philosopher's Stone" ; tit3 = "The Lion, the Witch and the Wardrobe" ; tit4 = "The Lord of the Rings"  ; tit5 = "Alice in Wonderland" 
#Create vars to store authors.
au1 = "Charles Dickens"  ; au2 = "J.K. Rowling" ; au3 = "C. S. Lewis" ; au4 = "J.R.R Tolkien"  ; au5 = "Lewis Carroll " 
#Create vars to store qty.
qty1 = 30 ; qty2 = 40; qty3 = 25 ; qty4 = 37 ; qty5 = 12

#Create tuples from the vars.
tup_vars = [(id1,tit1,au1, qty1),(id2,tit2,au2, qty2),(id3,tit3,au3, qty3),(id4,tit4,au4, qty4),(id5,tit5,au5, qty5)]



exists = cur.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table'
  AND name='CLERK'; """).fetchone()


while True:
    if exists[0] == 0 :
        print("Creating Table...")
        cur.execute(table)
        #Insert queries into the table.
        cur.executemany(""" INSERT INTO CLERK(ID, TITLE, AUTHOR, QTY) VALUES(?,?,?,?) """,
        tup_vars)
        db.commit()
        break

    else:
        print("Table loaded...")
        break




def clerk_menu():
    #Define the menu.
    ops = ("""
    Select one of the following Options:
    1   -   Enter Book
    2   -   Update Book 
    3   -   Delete Book
    4   -   Search Book
    0   -   Exit
    """)

    #While loop until input.
    while True:
        #Try/except to ensure input is valid.
        try:
            #User input their choice.
            menu_ = int(input(ops))
            #Assert condition makesure number is between 0 and 4.
            assert  0 <= menu_ <= 4, "valid"  
            #Return the choice if it is valid.
            return menu_


        #Except the input is not an integer.
        except ValueError:
            print("Please enter a number.")

        #The input is not an option.
        except AssertionError:
            print("The number must be between 0 and 4.")

#Define function to ensure number is input.
def inte():
    #While loop to get input.
    while True:
        #Try / except to ensure valid.
        try:

            num = int(input("Enter here:"))
            assert num > 0 
            return num

        except ValueError:
            #Print output.
            print("Error this field requires an integer, please enter a valid number.")

        except AssertionError:
            #Make sure number is not negative.
            print("Number most be positive.")


#Define function to ensure ID does not already exist.
def check_id(bk_id):
    #Check id existss.
    ID = bk_id
    cur.execute("""SELECT rowid FROM CLERK WHERE ID = ? """, (ID,))
    res = cur.fetchall()
    db.commit()
    #Return True if id exists and False if not.
    if len(res) == 0:
        return False
    else:
        return True


#Define function to check title exists.
def check_tit(tit):
    #title  is tit.
    title = tit
    #Check if it exists.
    cur.execute("""SELECT ID FROM CLERK WHERE TITLE LIKE ? """, (title, ))
    res = cur.fetchall()
    db.commit()
    #Return True if it exists and false if not.
    if len(res) == 0:
        return False
    else:
        return True



#Define function to check author exists.
def check_au(au):
    #Author is au.
    author = au
    #Check if it exists by 
    cur.execute("""SELECT ID FROM CLERK WHERE AUTHOR LIKE ? """, (author, ))
    #Res stores the length.
    res = cur.fetchall()
    #Commit to save progress.
    db.commit()
    #If len is 0 the author does not exists - return True or False depending on this.
    if len(res) == 0:
        return False
    else:
        return True


#Define function to get book details book.
def get_book():
    
    complete = False
    #Get book ID.
    print("First enter Book ID")
    #While to loop until input.
    while True:
        #Try except to ensure input is valid.
        try:
            #Get a valid integer.
            bkID = inte()
            #Check the ID does not exist.
            check = check_id(bkID)
            #Assert condition; that the id doesnt exist.
            assert check is False, "valid"

            #Get book title.
            bkTIT = input("Book Title: ")

            #Get book author.
            bkAU = input("Book Author: ")
            #Get book qty.
            print("Finally Enter the Quantity of Books")
            bkQTY = inte()

            #Save the details in a tuple.
            book_deets = (bkID, bkTIT, bkAU, bkQTY )
            #Return the tuple.
            return book_deets
            complete = True
        #Except if the ID already exists and let user re-enter a new ID.
        except AssertionError:
            print(f"The id {bkID} already exists, please enter a different one.")


#Define function to inset book.
def insert_book(tup):
    #Get a tupleinput.
    book = tup
    #Execute quest.
    cur.execute(""" INSERT INTO CLERK(ID, TITLE, AUTHOR, QTY) VALUES(?,?,?,?) """,
        book)
    #Output tells user request is fulfilled.
    print("Book Added")
    #Commit to save the progress.
    db.commit()





def check_y_n():
    #While checked is false.
    checked = False
    #Loop for input.
    while True:
        #Try get valid input.
        try:
            #Input.
            y_n = input("y/n :")
            #Assert condition.
            assert y_n in ("y", "n"), "valid"
            #If valid return answer.
            return y_n
            #Check is true.
            checked =True

        #Except if input is not y or n.
        except AssertionError:
            #Error message.
            print("Please enter 'y' for yes or 'n' for no.")

#Define function to find what part of the book they want to find/update.
def querey_what():
    #What is false until information is obtained.
    what = False
    #Loop until input.
    while True:
        #Try except - get valid input.
        try:
            quer = input("""
            q   -   quantity
            t   -   title
            a   -   author """).lower()

            #Assert condition.
            assert quer in ("q", "t", "a"), "valid"
            #If condition met.
            return quer
            #What is now true.
            what = True

        #Except condition not met.
        except AssertionError:
            print("Please enter one of the options provided.")


#Define function to find book from author or title.
def find_au_tit():

    print("Do you know the title or author of the book?")
    yn = check_y_n()

    while yn == "y":
        #Try except to get valid input.
        try:

            print("If you know the title enter 't' and if you know the author enter 'a', if you no neither enter 'i'.")

            tit_au = input("""
            t   -   title
            a   -   author : 
            i   -   identify another way """).lower()
            #Assert condition.
            assert tit_au in ("t", "a", "i"), "valid"
            #If user want to search by title.
            if tit_au == "t":
                #User inputs title.
                tit = input("Enter the title of the book:")
                #Check the title is valid.
                test = check_tit(tit)

                if test is True:
                    print("Title Exists")
                    print("What do you want to update?")
                    UPD = querey_what()
                    upD_title(tit, UPD)  
                    break

                else:
                    yn = "n"
            #User wants to find book by author.
            if tit_au == "a" :
                #Input author.
                au = input("Enter the authors name:")
                test = check_au(au)

                if test is True:
                    print("Author Exists")

                    print("What do you want to update?")
                    UPD = querey_what()  
                    upD_au(au, UPD)
                    break


                else:
                    yn = "n"
                

            if tit_au == "i":
                print("identify another way.")
                yn = "n"


        #If not a valid input.
        except AssertionError:
            #Print error message.
            print("Please enter one of the options.")
    while yn == "n":
        print("Printing all of the table!")
        cur.execute("SELECT * FROM CLERK") ; print(cur.fetchall())
        db.commit()
        update_bk()
        break

#find_au_tit()

#Update from title function.
def upD_title(title, upd) :

    TITLE = title

    if upd == "q":
        print("Update quantity!")

        print("New Quantity")
        QTY = inte()

        cur.execute("""UPDATE CLERK SET QTY = ? WHERE TITLE = ? """,(QTY, TITLE))
        print("Quantity updated!")
        db.commit()



    if upd== "t":
        print("Update Title!")

        title = input("Enter new title: ")

        cur.execute("""UPDATE CLERK SET TITLE = ? WHERE TITLE = ? """,(title, TITLE))
        print("Title updated!")
        db.commit()



    if upd == "a":
        print("Update Author!")

        author = input("Enter new author: ")
        cur.execute("""UPDATE CLERK SET AUTHOR = ? WHERE TITLE = ? """,(author, TITLE))
        print("Author updated!")
        db.commit()


#Update from author function.
def upD_au(author, upd) :

    AUTHOR = author

    if upd == "q":
        print("Update quantity!")

        print("New Quantity")
        QTY = inte()

        cur.execute("""UPDATE CLERK SET QTY = ? WHERE AUTHOR = ? """,(QTY, AUTHOR))
        print("Quantity updated!")
        db.commit()



    if upd== "t":
        print("Update Title!")

        title = input("Enter new title: ")

        cur.execute("""UPDATE CLERK SET TITLE = ? WHERE AUTHOR = ? """,(title, AUTHOR))
        print("Title updated!")
        db.commit()



    if upd == "a":
        print("Update Author!")

        author = input("Enter new author: ")
        cur.execute("""UPDATE CLERK SET AUTHOR = ? WHERE AUTHOR = ? """,(author, AUTHOR))
        print("Author updated!")
        db.commit()





#Define function to update book. - Only qty can be updated bc names/authers don't change?
def update_bk():

    #check if user knows book id.
    print("Do you know the ID of the book you wish to update?")
    #Get valid input.
    y_n = check_y_n()

    #Task is not complete.
    #complete = False
    #While loop until complete.
    while y_n == "y":
        #Try / except to check input is valid.
        try:
            #Output to tell user what to o.
            print("Enter book ID:")
            #Check input is a number.
            bkID = inte()
            #Check the ID exists.
            check = check_id(bkID)
            #Assert condition.
            assert check is True, "valid"
            ID = bkID
            #If condition is met.
            print("What would you like to update? ")
            #Find what they want to update.
            upd = querey_what()
            #If upd is q user wants to update qty.
            if upd == "q":
                #Output tells users whats happening.
                print("Update quantity!")
                #Print new qty so they know what to input.
                print("New Quantity")
                #Get a valid number from inte functon.
                QTY = inte()
                #Execute request.
                cur.execute("""UPDATE CLERK SET QTY = ? WHERE ID = ? """,(QTY, ID))
                #Output lets user know request has been fulfilled
                print("Quantity updated!")
                #Commit to save progress.
                db.commit()
                break


            #T means update title.
            if upd== "t":
                #Output
                print("Update Title!")
                #Get input.
                title = input("Enter new title: ")
                #Execute request.
                cur.execute("""UPDATE CLERK SET TITLE = ? WHERE ID = ? """,(title, ID))
                #Let user know its successful.
                print("Title updated!")
                #Commit to save progress.
                db.commit()
                break



            if upd == "a":
                #Update author.
                print("Update Author!")
                #Get input.
                author = input("Enter new author: ")
                #Execute request.
                cur.execute("""UPDATE CLERK SET AUTHOR = ? WHERE ID = ? """,(author, ID))
                #Output to let user know it is a success.
                print("Author updated!")
                #Commit t save progress.
                db.commit()
                break



        #Except if ID doesn't exist.
        except AssertionError:
            #Print error message.
            print("The ID you entered does not exist. ")
            #yn is now n which will find another way.
            y_n = "n"
            break

    while y_n == "n":
        print("Find another way...")
        #Find the book via author or title.
        find_au_tit()
        break


#Delete book function.
def del_book():
    #Find if user wants to delete from ID or not.
    print("Delete from ID? (if no delete from author or title) ")
    #Check input is valid.
    yn = check_y_n()

    while yn == "y":
        #Output.
        print("Enter ID number: ")
        #Input number.
        put_int = inte()
        #Check its a valid ID.
        val = check_id(put_int)

        #Assert condition.
        if val is True:
            #Delete book.
            ID = put_int
            #Execute request.
            cur.execute("""DELETE FROM CLERK WHERE ID = ? """, (ID, ))
            #Output to show success.
            print("Book deleted...")
            #Commit to save progress.
            db.commit()
            
            break

        else:
            yn = "n"
    #While yn is n.
    while yn == "n":
        #Try get valid input.
        try:
            #Output explains what to do.
            print("If you want to delete from the title enter 't' or the author enter 'a', if you know neither enter 'i'.")
            #Input option.
            tit_au = input("""
            t   -   title
            a   -   author : 
            i   -   identify another way """).lower()
            
            #Assert condition.
            assert tit_au in ("t", "a", "i"), "valid"
            #If user want to search by title.
            if tit_au == "t":
                #User inputs title.
                tit = input("Enter the title of the book:")
                #Check the title is valid.
                test = check_tit(tit)

                if test is True:
                    #Test is true means the title is valid and the book can be delted.
                    TITLE = tit
                    #Execute request.
                    cur.execute("""DELETE FROM CLERK WHERE TITLE = ? """, (TITLE, ))
                    #Output result.
                    print("Book deleted...")
                    #Commit to save.
                    db.commit()
                   
                    break
                
                else:
                    #yn = z to prinat all table so user can find the book details.
                    yn = "z"
                    break
            #User wants to find book by author.
            if tit_au == "a" :
                #Input author.
                au = input("Enter the authors name:")
                test = check_au(au)

                if test is True:
                    #Test is true means the title is valid and the book can be delted.
                    AUTHOR = au
                    cur.execute("""DELETE FROM CLERK WHERE AUTHOR = ? """, (AUTHOR, ))
                    #Output tells user result.
                    print("Book deleted...")
                    #Commit to save the progress.
                    db.commit()

                    break
                else:
                    #Else printall table and break.
                    yn = "z"
                    break

            if tit_au == "i":
                #I prints all table so user can get info.
                print("Identify another way.")
                yn = "z"


        #If not a valid input.
        except AssertionError:
            #Print error message.
            print("Please enter one of the options.")

    #While yn = z print the whole table and then let the user attempt to update book again with info.
    while yn == "z":
        cur.execute("SELECT * FROM CLERK") ; print(cur.fetchall())
        db.commit()
        update_bk()
        break

#Function to get input of what part user will want to edit or search by.
def ops():

    while True:
        try:
            search = input("""
            i   -   ID
            t   -   Title
            a   -   Author
            e       Exit
             """).lower()

            #Assert condition.
            assert search in ("i", "t", "a", "e"), "valid"

            return search
            break
        #Except invalid input.
        except AssertionError:
            #Error message.
            print("The input was invalid please enter one of the follwoing options.")




#Define function to know what to search for by.
def search_by():
    #What info to put into the search function.
    info = what_info()
    #If info is e then break loop.
    if info == "e": 
        complete = True; return complete

    #Output establish what the function is.
    print("""What do you want to search by?""")
    #Var to store what they want to search by.
    search_ = ops()
    complete = False

    while True:

        if search_ == "i":
        #Output explains whats to do.
            print("Enter the ID of the book you want to view")
            idd = inte()
            val = check_id(idd)
            #Check the id is valid.
            if val is True:
                #Save as id.
                ID = idd
                # Save search as by for putting into next function.
                by = search_
                #Function to complete request.
                search(info, by, ID)
                #One complete break the loop.
                complete = True ; return complete

            #If input is invalid break the loop.
            else:
                print("Invalid ID")
                complete = False
                return complete
        #Get user to input the title.    
        if search_ == "t":
            tit = input("Enter the title of the book: ")
            #Check title is valid.
            val = check_tit(tit)
            #If title valid complete request.
            if val is True:
                #Define vars.
                TITLE = tit
                by = search_
                #Use search function to look for info.
                search(info, by, TITLE)
                complete = True ; return complete
            #Invalid input breaks tyhe loop
            else:
                print("Invalid title")
                complete = False
                return complete


            #Repeat same function for author.
        if search_ == "a":
            au = input("Enter the author of the book:")
            val = check_au(au)

            if val is True:
                AUTHOR = au
                by = search_
                search(info, by, AUTHOR)
                complete = True ; return complete
            else:
                print("Invalid Author")
                complete = False
                return complete


            #If e is input exit function.
        if search_ == "e":
            complete = True
            return complete
    

#Function to find what info the user wants about the book.
def what_info():

    #Ask if they want all info.
    print("Do you want all infomation about the book?")
    #Get valid input.
    yn = check_y_n()
    #If user wants all info infor = all.
    if yn == "y":
        info = "all"
    #If not then find what info they want.
    if yn == "n" :
        print("What information do you want about the book?")
        #User ops function to find what information user wants about the book.
        info = ops()

    return info

#Function for searching.
def search(info, by, inp) :
    #Comp is false to keep loop running.
    comp = False
    #While loop to get input.
    while True:
        #save var as inpt
        inpt = inp
        #If user wants all info about the book.
        if info == "all":
            #If by is i they want to search for a book by the ID.
            if by == "i":
                #Execute the users request.
                cur.execute("""SELECT * FROM CLERK WHERE ID = ? """, (inpt, ))
                print(cur.fetchall())
                #Commit to save progress.
                db.commit()
                #Comp is True break the loop.
                comp = True 
                return comp     
                break
            if by == "t":
                #If by is T they want to search by title.
                cur.execute("""SELECT * FROM CLERK WHERE TITLE = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break

                #If by is a they want to seach by author.
            if by == "a":
                cur.execute("""SELECT * FROM CLERK WHERE AUTHOR = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break
                
            #search for all
            #If info is i user wants to just find the ID of the book. 
        if info == "i":
            #Execute users request by is the information theyre using to search for the book.

            if by == "i":
                #Invalid function to look for the id of a book by its id.
                print("Invalid function")
                comp = True 
                return comp               
            if by == "t":
                cur.execute("""SELECT ID FROM CLERK WHERE TITLE = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break
            #Search by author.
            if by == "a":
                cur.execute("""SELECT ID FROM CLERK WHERE AUTHOR = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break

            
            #Info is t the user wants to know the title.
        if info == "t":
            #The user will use the id to look for the ook title.
            if by == "i":
                cur.execute("""SELECT TITLE FROM CLERK WHERE ID = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break

            if by == "t":
                #Invalid to search for book title using the book title.
                print("Invalid function")
                #Loop is broken.
                comp = True 
                return comp                
            if by == "a":
                cur.execute("""SELECT TITLE FROM CLERK WHERE AUTHOR = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break

            
            #Search for the author by...
        if info == "a":
            #By the id.
            if by == "i":
                cur.execute("""SELECT AUTHOR FROM CLERK WHERE ID = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break
            #By the title.
            if by == "t":
                cur.execute("""SELECT AUTHOR FROM CLERK WHERE TITLE = ? """, (inpt, ))
                print(cur.fetchall())
                db.commit()
                comp = True 
                return comp     
                break
            #By author is invalid - break the loop.
            if by == "a":
                print("Invalid function")
                comp = True 
                return comp
                
        #If info is e break the loop.
        if info == "e": 
            #exit
            comp = True; return comp

    


#Menu should include:
""" 1. Enter book x insert_book(ins_get_book())
2. Update book x
3. Delete book x
4. Search books x
0. Exit
"""
#Print program name.
print("Book Clerk Program!")

#Output name.
print("MENU")

choice = " "

#While choice doesn't =0 loop the menu.
while choice != 0:
    #Get user option.
    choice = clerk_menu()

    if choice == 1:
        #Output tells user what function will do.
        print("Enter Book!")
        #Use insert book function to insert the book, and the get_book function to get the details.
        insert_book(get_book())

    if choice == 2:
        #Output tells user what function will do.
        print("Update Book")
        #Use the update book function.
        update_bk()

    if choice == 3:
        #Output tells user what function will do.
        print("Delete Book")
        #Use the delete book function.
        del_book()
        
    if choice == 4:
        #Output tells user what function will do.
        print("Search")
        #Use the search function.
        search_by()

    if choice == 0:
        #Output tells user what function will do.
        print("Goodbye!")
        exit()

    
    

