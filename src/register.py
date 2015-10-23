"""
register.py - handles registering of new users
From project specifications: Unregistered users should be able to sign up by providing an email and a password.
"""
import getpass 
import menuHandler
import main

def handleRegister():
    # ask for email and password
    print("Please register your email and password.\n")
    user_email = input("Email: ")
    user_pw = getpass.getpass()

    # queries
    checkIfUserExists = "SELECT email FROM users WHERE email = '" + user_email + "'"
    addToUsers = "INSERT INTO users VALUES('" + user_email + "', '" + user_pw + "', SYSDATE)"
    commit = "commit"

    # check if user exists
    db = main.getDatabase()
    db.execute(checkIfUserExists)
    user_results = db.cursor.fetchall()
    if len(user_results) > 0: # user exists!
        print("User already exists. Please log in.\n")
        main.showMainMenu()
    elif (len(user_pw) > 4):
        print("Password must NOT be more than 4 characters.")
        handleRegister()
    else:   # everything is valid!
        db.execute(addToUsers)
        db.execute(commit)   
        print("You've successfully registered! Please log in.\n")
    