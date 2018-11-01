from sys import exit
from getpass import getpass
import re
import sqlite3

connection = None
cursor = None

def main():  
    Login = True
    
    path= "./pr1.db"
    connect(path)
    
    
    connection.commit()
    connection.close()

    while(Login):
        Login = False
        userDetails = LoginWindow()
        if userDetails != False:
            Login = MainMenu(userDetails)

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def MainMenu(user):

    while(True):
        print("Logged in as: " + user[0])
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
            print("Logged our from account: " + user[0])
            return True
        elif userInput == "7":
            ExitProgram()
        else:
            print("LOL chose a valid choice")


def ExitProgram():
    print("Program Exited")
    exit()      

def LoginWindow():

    # User may choose to login or register
    # The program loops until user enters a valid choice
    # Value holds the return from the functions
    # When value is false, it means user wanted to return to main menu

    while(1):
        print(" 1. Login")
        print(" 2. Register")
        print(" 3. Exit")
        num = True

        UserChoice = input("Enter you choice: ")

        while(num):   
            if UserChoice == "1":
                value = getUserDetails("Returning")
                if (value != "False"): 
                    return value

            if UserChoice == "2":
                value = getUserDetails("New")
                if (value != "False"):
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
        print("type 'return' to return to the login options")
        email = input("Enter your email address: ")

        if email == "return":
            return False

        if EmailNotValid(email):
            print("\nInvalid email Address. Please try again.")
            continue

        password = getpass("Password: ")       

        if status == "New":
            # Add New Use
            name = input("name: ")
            phone = input("phone: ")
            return (email, password, name, phone)
        else:
            userExists = True
            # Check if user exists in database
            if (userExists):
                return (email, password)
            print("Wrong email and password combination. Please try again.")



def EmailNotValid(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        return True         
    else:
        return False 

def OfferRide(User):
    return 

def SearchRide(user):
    return 

def BookOrCancel(user):
    return

def RideRequest(user):
    return

def SearchDeleteRequest(user):
    return


main()
