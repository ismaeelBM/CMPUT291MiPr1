from sys import exit
from getpass import getpass
import re
import sqlite3
import sys
import datetime

conn = None
cur = None

def main():  
    # Main function of the program. Gets the database file from argument.
    # Then asks user to login
    Login = True
        
    if len(sys.argv) == 2:
        path = sys.argv[1]
        connect(path)
    
    else:
        print("Invalid Command Line Argument")       
        return

    while(Login):
        Login = False
        userDetails = LoginWindow()
        if userDetails != False:
            Login = MainMenu(userDetails)

def connect(path):
    # This function is responsible for setting the database
    
    global conn, cur

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return

def MainMenu(user):
    # MainMenu: Provides te user with options to:
    # 1. Offer Rides, 2. Search Rides, 3. Make/Cancel Bookings, 
    # 4. Post Ride Requests 5. Search/Delete Ride Requests
    # 6. Log Out 7. Close Program
    
    
    while(True):
        print("\n\n-------------------- Main Menu ----------------------")
        printMessages(user)
        print("Logged in as: " + user)
        print("1. Offer Ride")
        print("2. Search Rides")
        print("3. Book Members/Cancel Booking")
        print("4. Post Ride Request")
        print("5. Search/Delete Ride Requests")
        print("6. Log Out")
        print("7. Close Program\n")

        userInput = input("Enter your Choice: ").lower()

        if userInput == "1":
            OfferRide(user)
        elif userInput == "2":
            SearchRide(user)
        elif userInput == "3":
            BookOrCancel(user)
        elif userInput == "4":
            RideRequest(user)
        elif userInput == "5":
            SearchDeleteRequest(user)
        elif userInput == "6":
            print("Logged out from account: " + user)
            return True
        elif userInput == "7":
            ExitProgram()
        else:
            print("LOL chose a valid choice")


def ExitProgram():
    # This function quits the program
    print("Program Exited")
    conn.commit()
    conn.close()    
    exit()      

def LoginWindow():

    # User may choose to login or register
    # The program loops until user enters a valid choice
    # Value holds the return from the functions
    # When value is false, it means user wanted to return to main menu

    while(1):
        print("\n\n-------------------- Login Window ----------------------")
        print(" 1. Login")
        print(" 2. Register")
        print(" 3. Exit")
        num = True

        UserChoice = input("Enter you choice: ").lower()

        while(num):   
            if UserChoice == "1":
                value = getUserDetails("Returning")
                if (value != False): 
                    return value

            if UserChoice == "2":
                value = getUserDetails("New")
                if (value != False):
                    return value      

            if UserChoice == "3":
                ExitProgram()
                num = False
            else:
                print("Please enter a valid option!")
                num = False



def getUserDetails(status):
    # This function gets the login/Register details from the user
    
    while True:
        print("\n\n-------------------- Details Entry ----------------------")
        print("type 'return' to return to the login options")
        email = input("Enter your email address: ").lower()
        
        
        if email == "return":
            return False
        

        
        if EmailNotValid(email):
            print("\nInvalid email Address. Please try again.")
            continue

        password = getpass("Password: ") 
        userExists = CheckUserExistence((email,password))
        if userExists and status == 'New':
            print('The email is already in use')
            continue        

        if status == "New":
            # Add New User
            
            name = input("name: ")
            phone = input("phone: ")
            AddMember((email, name, phone, password))
            return email
        else:
            userExists = CheckUserExistence((email,password))
            # Check if user exists in database
            if (userExists):
                return email
            print("Wrong email and password combination. Please try again.")

def printMessages(user):
    # This function prints all unseen messages when the user logs in
    print(user)
    cur.execute("SELECT content FROM inbox WHERE email = ? AND seen = 'n';", (user,) )
    rows = cur.fetchall()
    
    i = 1
    if len(rows) == 0:
        print("No new messages \n")
    else:
        print("Unread Messages \n")
    for message in rows:
        print(str(i) + ') ' + message[0] + '\n')
        i += 1
        
    cur.execute("UPDATE inbox SET seen = 'y' WHERE email = ?;", (user,))
    return      


def EmailNotValid(email):
    # This function checks if the email is valid
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        return True         
    else:
        return False 

def OfferRide(email):
    # This function allows the member to offer a ride and add it to the database
    
    
    cur.execute("Select cno From cars WHERE owner = ?;",(email,))
    carList = cur.fetchall()
    if len(carList) <= 0:
        print("Sorry you don't have any cars registered to offer rides")
        return
    
    print(carList[0][0])
    
    notvalid = True
    while notvalid:
        
        date = input("Enter ride date(yyyy/mm/dd): ")
        
        isValidDate = True  
        try : 
            year,month,day = date.split("/")
            if datetime.datetime(int(year),int(month),int(day)) < datetime.datetime.today():
                isValidDate = False
            
        except ValueError :
            isValidDate = False
        
        if (isValidDate):
            notvalid = False
        else :
            print ("Date is Invalid..")    
            notvalid = True
            
    notvalid = True     
    while notvalid:
        seats = input("Enter number of seats offered: ")
        try:
            seats = int(seats)
            notvalid = False
        except ValueError:
            print("Number of seats is Invalid..")
            notvalid = True
        
    notvalid = True         
    while notvalid:
        price = input("Enter price per seat:$ ") 
        try:
            price = int(price)
            notvalid = False 
        except ValueError:
            print("Price per seat is Invalid..") 
            notvalid = True
           

        
    luggage = input("Enter luggage description: ").lower()
    
    srcLocation = None
    while srcLocation == None:
        srcLocation = input("Enter a source location: ").lower()
        srcLocation = locationFinder(srcLocation)
    
    srcLocation = srcLocation[0]
    
    srcDestination = None
    while srcDestination == None:
        srcDestination = input("Enter a destination location: ").lower()
        srcDestination = locationFinder(srcDestination)
    
    srcDestination = srcDestination[0]
    enroute = []
    
    while True:
        setLocation = input("Enter an enroute location (leave blank and press enter to skip): ").lower()
        if setLocation == '':
            break     
        setLocation = locationFinder(setLocation)
        if setLocation == None:
            continue
        else:
            enroute.append(setLocation[0])

    while True:
        if len(carList) > 1:
            carNo = input("Enter car number: ")
            if (carNo,) not in carList:
                print("The car number does not exist in your existing cars")
                continue
        else:
            carNo = carList[0][0]
            print("Car number set to " + str(carNo))
            break
    
    
    cur.execute("SELECT rno FROM rides;")
    rides = cur.fetchall()
    alist = []
    for number in rides:
        alist.append(int(number[0]))
    
    rno = max(alist) + 1
    
    ridesRecord = (rno, price, date, seats, luggage, srcLocation, srcDestination, email, carNo)
    cur.execute("INSERT INTO rides VALUES (?,?,?,?,?,?,?,?,?);", ridesRecord)
    
    for route in enroute:
        enrouteRecord = (rno, route)
        cur.execute("INSERT INTO enroute VALUES (?,?);", enrouteRecord)
        conn.commit()
    
    print("Your ride has been added to the database")
    return

def locationFinder(code):
    # This function is used to search for all location that matches the keyword provided
    
    cur.execute('Select lcode From locations;')
    rows = cur.fetchall()
    if ((code,) in rows):
        return (code,)
    else:
        arg = "SELECT * FROM locations WHERE city like '%" + code + "%' OR prov like '%" + code + "%' or address like '%" + code + "%';"
        cur.execute(arg)
        rows = cur.fetchall()
        if len(rows) == 0:
            print("No similar locations found")
            return
        choice = getChoice(rows)
        return choice
        
def getChoice(rows, showAll = False):
    # This function displays all the record in rows if showAll is true
    # else it shows 5 records at a time
    
    n = 0
    j = 0   
    
    while True:
        if showAll:
            for i in range(0, len(rows)):
                if i >= len(rows):
                    break
                print(str(i + 1) + ') ', rows[i])
        else:
            for i in range(n, n + 5):
                if i >= len(rows):
                    break
                print(str(i + 1) + ') ', rows[i])
    
            if (n + 5) < len(rows):
                print("Enter 'M' to show more options")
            else:
                print("End of search reached. Enter 'M' to show from beginning")
        
        print("Enter 'return' to go back")
        
        choice = input("Enter your choice: ").lower()
        
        if choice == 'return':
            return
        elif choice == 'M' and showAll == False:
            if (n+5) < len(rows):
                n = n + 5
                continue
            else:
                n = 0
                continue
        else:
            try:
                choice = int(choice)
                if choice < len(rows) + 1 and choice >= 1:
                    print (rows[choice-1])
                    return (rows[choice-1])
                    
                else:
                    print("Please enter a valid option.")
                    continue                        
                    
            except:
                print("Please enter a valid option.")
                continue

    
def SearchRide(user):
    # This function allows the user to find a ride
    
    keywords = input("Enter from 1-3 keywords seperated by whitespace: ").lower()
    keywords.lstrip()
    keywords.rstrip()
    keyword = keywords.split(" ")
    keyword = keyword[:3]
    
    arg = []
    i = 1
    for key in keyword:
        value = "select rno from ( " + addArg(key) + ") as key" + str(i)
        arg.append(value)
        i += 1
    
    arg = " Intersect ".join(arg)
    
    arg = "select rno, driver, price, rdate, seats, lugDesc, src, lcode as onroute, dst  from rides natural left outer join enroute where rno in(" + arg
    arg = arg + ");"
    
    cur.execute(arg)
    rows = cur.fetchall()
    
    if len(rows) == 0:
        print("No matching records found")
        return
    choice = getChoice(rows)
    
    if choice == None:
        return
    else:
        message = input("Enter your message to the driver: ")
        cur.execute("SELECT datetime('now','localtime');")
        date = cur.fetchone()[0]      
        arg = (choice[1],date,user,message,choice[0],'n')
        cur.execute("insert into inbox values (?, ?, ?, ?, ?,?);", arg)     
        print("Your Message has been sent")
    
    
    return 

def addArg(key):
    # This function helps generate the query for finding a match with the keyword
    
    commonCheck = "(l.lcode = '" + key + "' or city like '%" + key + "%' or prov like '%" + key + "%'  or address like '%" + key + "%')"
    
    check1 = "Select rno from rides, locations l where src = lcode and "
    check2 = "Union Select rno from rides, locations l where dst = lcode and "
    check3 = "union Select rno from enroute e, locations l where e.lcode = l.lcode and"
    
    arg = check1 + commonCheck + check2 + commonCheck + check3 + commonCheck
    
    return arg

def BookOrCancel(user):
    # This function allows the user to either choose to make or cancel a booking
    
    notvalid = True
    while notvalid:
        print("To book ride, Enter 1")
        print("To cancel ride, Enter 2")
        print("To exit, Enter 3")

        userInput = input().lower()
                
        if userInput == "1":
            book(user)
            return False

        elif userInput == "2":
            cancel(user)
            return False

        elif userInput == "3":
            return False
        
        else:
            print("Invalid input!")
            return False

def book(user): 
    # This function allows the user to make a booking
    
    cur.execute(''' SELECT r.rno, r.seats-ifnull(sum(b.seats),0) 
                            FROM rides r, bookings b 
                            WHERE b.rno = r.rno and r.rno in
                                            (SELECT rno 
                                             FROM rides 
                                             WHERE driver = 'don@mayor.yeg')
                                             GROUP BY r.rno''')
    rows = cur.fetchall()
    rno = getChoice(rows)    
    
    booking = True
    while booking:
        
        cur.execute("SELECT bno FROM bookings;")
        bookings = cur.fetchall()
        alist = []
        for number in bookings:
            alist.append(int(number[0])) 
        bno = max(alist) + 1  
        
        email = input("Enter member's email: ").lower()
        cur.execute("SELECT email FROM members;")
        listemails = cur.fetchall() 
        while (email,) not in listemails:
            print("This email is not registered")
            email = input("Enter member's email: ").lower()
        
        cost = input("Enter cost of ride: ")
        if cost == '':
            cost = None
        
        
        while True:
            seats = input("Enter number of seats to book: ")
            if rno[1] < int(seats):
                decision = input("The ride is overbooked by " + str(int(seats) - rno[1]) + " seats! Are you sure you want to continue? (y/n)").lower()
                if decision == 'y':
                    break
                elif decision == 'n':
                    return
                else:
                    print("Invalid Input")
                    continue
            else:
                break
                
                 
        pickup = input("Enter pickup location: ").lower()
        if pickup == '':
            pickup = None
        else:
            pickup = locationFinder(pickup)
            if pickup != None:
                pickup = pickup[0]
        
        dropoff = input("Enter dropoff location: ").lower()
        if dropoff == '':
            dropoff = None
        else:        
            dropoff = locationFinder(dropoff)
            if dropoff != None:
                dropoff = dropoff[0]

        arg = (bno,email,rno[0],cost,int(seats),pickup,dropoff)
        cur.execute("insert into bookings values (?,?,?,?,?,?,?);", arg)
        
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M")
        message = ("Your booking has been cancelled!")
        status = "n"
        arg = (email,date,user,message,rno[0],status)   
        print("You have been booked for ride no. " + rno[0])
        
        conn.commit()
        return False 
            
        
        
    
    return      

def cancel(user):
    # This function allows user to cancel a booking
    
    now = datetime.datetime.now()
    cur.execute(''' SELECT b.bno, email, r.rno
                    FROM bookings b, rides r
                    WHERE r.rno = b.rno
                    and driver = ?''',(user,)) 
    rows = cur.fetchall()
    delete = getChoice(rows,True)
    cur.execute("DELETE FROM bookings WHERE bno = ?;",(delete[0],))

    date = now.strftime("%Y-%m-%d %H:%M")
    message = ("LOL, your booking has been cancelled!")
    status = "n"
    arg = (delete[1],date,user,message,delete[2],status)
    cur.execute("insert into inbox values (?, ?, ?, ?, ?,?);", arg)
    print("The booking no.",delete[0],"has been cancelled.")
    
    conn.commit()
    return

def checkList(sqlSelect, sqlFrom, sqlWhere = '', item = None):
    # If item is none, return the query 'Select sqlSelect FROM sqlFrom sqlWhere'
    # If item is not none, checks whether item exists in the previously mentioned query
    
    arg = "Select " + sqlSelect + " FROM " + sqlFrom + sqlWhere + ";"
    cur.execute(arg)
    rows = cur.fetchall()
    if item == None:
        return rows
    else:
        return ((item,) in rows)

def RideRequest(user):
    # This function allows the member to post a ride request
    
    notvalid = True # For checking date validity
    while notvalid:
        date = input("Enter ride date(yyyy/mm/dd): ")
        isValidDate = True 

        try :   
            year,month,day = date.split("/")
            if datetime.datetime(int(year),int(month),int(day)) < datetime.datetime.today():
                isValidDate = False
            
        except ValueError :
            isValidDate = False
        
        if (isValidDate):
            notvalid = False
        else :
            print ("Date is Invalid..")    
            notvalid = True
         
    cur.execute("SELECT rid FROM requests;")
    request = cur.fetchall()
    alist = []
    for number in request:
        alist.append(int(number[0])) 
    rid = max(alist) + 1              
    
    pickup = None
    while pickup == None:
        pickup = input("Enter a pickup location: ").lower()
        pickup = locationFinder(pickup)
    
    pickup = pickup[0]        
    
    dropoff = None
    while dropoff == None:
        dropoff = input("Enter a source location: ").lower()
        dropoff = locationFinder(dropoff)
    
    dropoff = dropoff[0] 

    while notvalid:
        price = input("Enter price:$ ") 
        try:
            price = int(price)
            notvalid = False 
        except ValueError:
            print("The price entered is Invalid..") 
            notvalid = True
    
    args = (rid,user,date,pickup,dropoff,price)
    cur.execute("insert into requests values (?,?, ?, ?, ?, ? );", args)
    print("Request added to database!")
    conn.commit()        
    return


def SearchDeleteRequest(user):
    # Here the Members can:
    # 1) Delete a ride they offered
    # 2) View ride requests and send message to a member regarding a request
    
    
    valid = True
    while valid:
        print("------------ Requests ------------------")
        print("To delete a request, Enter 1")
        print("To view requests (and send message), Enter 2")
        print("To exit, enter 3")
        
        userInput = input().lower()
                
        if userInput == "1":    
            cur.execute(''' SELECT rid, email, rdate, pickup, dropoff, amount
                            FROM requests 
                            WHERE email = ?''',(user,)) 
            rows = cur.fetchall()
            if len(rows) <= 0:
                print("No ride request\n")
                return False
            else: 
                delete = getChoice(rows,True)                      
                cur.execute("DELETE FROM requests WHERE rid = ?;",(delete[0],))    
                print("Request Deleted")
                conn.commit()  
                return False
                
        elif userInput == "2":
            location = input("Enter pickup location(city/lcode): ").upper()
            cur.execute('Select rid, email, rdate, pickup, dropoff, amount From requests, locations where pickup = lcode and (UPPER(pickup) =? or UPPER(city) = ?);',(location,location))
            rows = cur.fetchall()
            if len(rows) <= 0:
                print("No records found")
                return
            else: 
                request = getChoice(rows,True)
            
            if request == None:
                continue
            
            message = input("Enter your message: ")
            while True:
                rno = input("Enter ride number associated with message: ")
                exist = checkList('rno', 'rides','',int(rno))
                if exist:
                    break
                else:
                    print("Sorry, the ride number does not exist in the database")
            
            cur.execute("SELECT datetime('now','localtime');")
            date = cur.fetchone()[0]  
            arg = (request[1],date,user,message,rno,'n')
            cur.execute("insert into inbox values (?, ?, ?, ?, ?,?);", arg)  
            print("Message Sent!\n")
            conn.commit()
            
        elif userInput == "3":
            return False
        
        else:
            print("Invalid input!")
            continue      
            
    return

def AddMember(memberDetails):
    # memberDetails contains a tuple with email and password
    # This fucntion Adds a new member with details from memberDetails to the database
    cur.execute("INSERT INTO members VALUES (?,?,?,?);", memberDetails)
    return

def CheckUserExistence(userDetails):
    # userDetails contains the password and email
    # Used to check if a certain user exists in the database
    
    cur.execute('Select email,pwd From members;')
    rows = cur.fetchall()
    if (userDetails in rows):
        return True
    else:
        return False
    

main()