"""
login.py -- handles user login to the system
From the specification: Registered users should be able to login using a valid email and password, respectively referred to as email and pass in table users.
"""

import getpass 
import menuHandler
import main

def handleLogin():
    # ask for email and password
    user_email = input("Email: ")
    user_pw = getpass.getpass()

    # check table if user exists
    #print(user_email + " " + user_pw)
    checkIfUserExists = "SELECT email FROM users WHERE email = '" + user_email + "' AND pass = '" + user_pw + "'"
    checkIfAgent = "SELECT email FROM airline_agents WHERE email = '" + user_email + "'"

    # check if user exists
    db = main.getDatabase()
    db.execute(checkIfUserExists)
    user_results = db.cursor.fetchall()
    for x in user_results: print(x)
    if len(user_results) > 0: # user exists!
        db.execute(checkIfAgent)
        agent_results = db.cursor.fetchall()
        if len(agent_results) > 0:
            menuHandler.handleAgentMenu(user_email)
        else: menuHandler.handleUserMenu(user_email)
    else: 
        print("User does not exist.")
        main.showMainMenu()
