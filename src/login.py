"""
login.py -- handles user login to the system
From the specification: Registered users should be able to login using a valid email and password, respectively referred to as email and pass in table users.
"""

import getpass 

def handleLogin():
	# ask for email and password
	user_email = input("Email: ")
	user_pw = getpass.getpass()

	# check table
	#print(user_email + " " + user_pw)


