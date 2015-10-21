"""
register.py - handles registering of new users
From project specifications: Unregistered users should be able to sign up by providing an email and a password.
"""

def handleRegister(connection):
    # ask for email and password
    print("Please register your email and password.\n")
    user_email = input("Email: ")
    user_pw = getpass.getpass()

    # check table:users if user already exists
    #print(user_email + " " + user_pw)

    # if not, add to table:users with user name and password provided
    