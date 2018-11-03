from sys import exit
from getpass import getpass
import re
import sqlite3
import sys
import datetime

conn = None
cur = None

def main():  
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
    global conn, cur

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return

def MainMenu(user):

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
        print("7. Close Program")

        userInput = input("Enter your Choice: ")

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

        UserChoice = input("Enter you choice: ")

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
    # For getting Login details
#    valid = True
    while True:
        print("\n\n-------------------- Details Entry ----------------------")
        print("type 'return' to return to the login options")
        email = input("Enter your email address: ")

        if email == "return":
            return False

        if EmailNotValid(email):
            print("\nInvalid email Address. Please try again.")
            continue

        password = getpass("Password: ")       

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
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        return True         
    else:
        return False 

def OfferRide(email):
    
    cur.execute("Select cno From cars WHERE owner = ?;",(email,))
    carList = cur.fetchall()
    if len(carList) <= 0:
        print("Sorry you don't have any cars registered to offer rides")
        return
    
    print(carList[0][0])
    
    notvalid = True
    while notvalid:
        date = input("Enter ride date(yyyy/mm/dd): ")
        year,month,day = date.split("/")
    
        isValidDate = True  
        try :   
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
           

        
    luggage = input("Enter luggage description: ")
    
    srcLocation = None
    while srcLocation == None:
        srcLocation = input("Enter a source location: ")
        srcLocation = locationFinder(srcLocation)
    
    srcDestination = None
    while srcDestination == None:
        srcDestination = input("Enter a destination location: ")
        srcDestination = locationFinder(srcDestination)
    
    enroute = []
    
    while True:
        setLocation = input("Enter an enroute location (leave blank and press enter to skip): ")
        if setLocation == '':
            break     
        setLocation = locationFinder(setLocation)
        if setLocation == None:
            continue
        else:
            enroute.append(setLocation)

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
    
    print("Your ride has been added to the database")
    return

def locationFinder(code):
    # Returns location for 
    
    cur.execute('Select lcode From locations;')
    rows = cur.fetchall()
    if ((code,) in rows):
        return code
    else:
        arg = "SELECT * FROM locations WHERE city like '%" + code + "%' OR prov like '%" + code + "%' or address like '%" + code + "%';"
        cur.execute(arg)
        rows = cur.fetchall()
        if len(rows) == 0:
            print("No similar locations found")
            return
        choice = getChoice(rows)
        return choice
        
def getChoice(rows):
        n = 0
        j = 0
        
        while True:
            for i in range(n, n + 5):
                if i >= len(rows):
                    break
                print(str(i + 1) + ') ', rows[i])
        
            if (n + 5) < len(rows):
                print("Enter 'M' to show more options")
            else:
                print("End of search reached. Enter 'M' to show from beginning")
            
            print("Enter 'return' to go back")
            
            choice = input("Enter your choice: ")
            
            if choice == 'return':
                return
            elif choice == 'M':
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
                        return (rows[choice-1][0])
                        
                    else:
                        print("Please enter a valid option.")
                        continue                        
                        
                except:
                    print("Please enter a valid option.")
                    continue
    
    
def SearchRide(user):
    return 

def BookOrCancel(user):
    return

def RideRequest(user):
    return

def SearchDeleteRequest(user):
    return

def AddMember(memberDetails):
    
    cur.execute("INSERT INTO members VALUES (?,?,?,?);", memberDetails)
    return

def CheckUserExistence(userDetails):
    cur.execute('Select email,pwd From members;')
    rows = cur.fetchall()
    if (userDetails in rows):
        return True
    else:
        return False
    

main()
