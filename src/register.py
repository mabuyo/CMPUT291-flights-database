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

    # queries
    checkIfUserExists = "SELECT email FROM users WHERE email = '" + user_email + "' AND pass = '" + user_pw + "'"
    addToUsers = "INSERT INTO users VALUES('" + user_email + "', '" + user_pw + "', SYSDATE)"
    commit = "commit"

    # check if user exists
    db = main.getDatabase()
    db.execute(checkIfUserExists)
    user_results = db.cursor.fetchall()
    if len(user_results) > 0: # user exists!
    	print("User already exists. Please log in.")
    	main.showMainMenu()
    else: 
        db.execute(addToUsers)
        db.execute(commit)   