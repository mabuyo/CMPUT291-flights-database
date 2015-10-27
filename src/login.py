"""
login.py -- handles user login to the system
From the specification: Registered users should be able to login using a valid email and password, respectively referred to as email and pass in table users.
"""

import getpass 
import main
import userMenu_Michelle as userMenu
import agentMenu

def handleLogin():
    # ask user for email and password
    user_email = input("Email: ")
    user_pw = getpass.getpass()

    # queries
    checkIfUserExists = "SELECT email FROM users WHERE email = '" + user_email + "' AND pass = '" + user_pw + "'"
    checkIfAgent = "SELECT email FROM airline_agents WHERE email = '" + user_email + "'"

    # check if user exists
    db = main.getDatabase()
    db.execute(checkIfUserExists)
    user_results = db.cursor.fetchall()
    if len(user_results) > 0: # user exists!
        db.execute(checkIfAgent)
        agent_results = db.cursor.fetchall()
        if len(agent_results) > 0:
             menu = agentMenu.AgentMenu(user_email)
        else:
            menu = userMenu.UserMenu(user_email)
        menu.showMenu()
    else: 
        print("User does not exist or password is incorrect.")
        main.showMainMenu()
