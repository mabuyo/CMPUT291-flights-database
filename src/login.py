"""
login.py -- handles user login to the system
From the specification: Registered users should be able to login using a valid email and password, respectively referred to as email and pass in table users.
"""

import getpass 
import menuHandler

def handleLogin(connection):
    # ask for email and password
    user_email = input("Email: ")
    user_pw = getpass.getpass()

    # check table if user exists
    #print(user_email + " " + user_pw)

    # if not, print error message and go back

    # if yes, check if airline agent

    # if airline agent, go to airline agent menu
    menuHandler.handleAgentMenu(connection)

    # if normal user, go to normal user menu
    menuHandler.handleUserMenu(connection)
