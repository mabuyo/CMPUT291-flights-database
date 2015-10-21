import sys
import cx_Oracle
import getpass 
from sqlite3 import OperationalError

# project packages
import login

def executeScriptsFromFile(filename, connection):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # initialize cursor
    curs = connection.cursor()

    try:
        #Execute each command 
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        for command in sqlCommands:
            try:
                curs.execute(command)
            except OperationalError as  msg:
                print("Command skipped: ", msg)

        cursInsert = connection.cursor()
        connection.commit()                      

        rows = curs.fetchall()
        for row in rows:
            print(row)                      

        curs.close()
        cursInsert.close()
        connection.close()

    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message) 

       # Execute every command from the input file
    print("Success!") 

def startConnection():
	"""
	Returns a the connection to the database.
	"""
    # get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user=getpass.getuser()

    # get password
    pw = getpass.getpass()

    # The URL we are connnecting to
    connStr = ''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'

    try: 
        # Make the connection 
        connection = cx_Oracle.connect(connStr)

    except cx_Oracle.DatabaseError as exc:
        error = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)

    return connection

def main():
    connection = startConnection()
	# TODO: take this out before submitting!!! this is solely for testing purposes
    executeScriptsFromFile('../res/prj_tables.sql', connection)  

    # main screen, ask to login, register or exit
    while True:
        userStart = input("Login, Register or Exit? ")

        if (userStart == "login" or userStart == 'L'): 
            login.handleLogin()
        elif (userStart == "register" or userStart == 'R'): 
            register.handleRegister()
        elif (userStart == "exit" or userStart == 'E'):
            sys.exit("You have logged out of the program.")
        else: print ("Please select one of the options. \n")

if __name__ == "__main__":
    main()
