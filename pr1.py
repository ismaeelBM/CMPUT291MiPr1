from sys import exit
from getpass import getpass
import re
import sqlite3
import sys

conn = None
cursor = None

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
    global conn, cursor

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
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
    cursor.execute("SELECT content FROM inbox WHERE email = ? AND seen = 'n';", (user,) )
    rows = cursor.fetchall()
    
    i = 1
    print("Unread Messages \n")
    print(rows)
    for message in rows:
        print(str(i) + ') ' + message[0] + '\n')
        i += 1
        
    cursor.execute("UPDATE inbox SET seen = 'y' WHERE email = ?;", (user,))
    return    


def EmailNotValid(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        return True         
    else:
        return False 

def OfferRide(User):
    notvalid = True
    while notvalid:
        date = input("Enter ride date(dd/mm/yy): ")
        day,month,year = date.split("/")
    
        isValidDate = True  
        try :   
            datetime.datetime(int(year),int(month),int(day))
        except ValueError :
            isValidDate = False
            
        if(isValidDate) :
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
    srcLocation = input("Enter source location: ")
    srcDestination = input("Enter source destiation: ")
    carNo = input("Enter car number(to skip, leave blank and press enter): ")
    
    
    enoute = []
    while True:
        setLocatoion = input("Enter a set of enroute locations:  ")
        if setLocatoion == '':
            break
        else:
            enoute.append(setLocatoion)   
        
    
    print("date: " +str(date), "price: $" +str( price), "luggage: "+str(luggage))
    return

def SearchRide(user):
    return 

def BookOrCancel(user):
    return

def RideRequest(user):
    return

def SearchDeleteRequest(user):
    return

def AddMember(memberDetails):
    
    cursor.execute("INSERT INTO members VALUES (?,?,?,?);", memberDetails)
    return

def CheckUserExistence(userDetails):
    cursor.execute('Select email,pwd From members;')
    rows = cursor.fetchall()
    if (userDetails in rows):
        return True
    else:
        return False
    

main()
