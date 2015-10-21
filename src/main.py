import sys
import cx_Oracle
import getpass 
from sqlite3 import OperationalError

# project packages
import login
import register

def executeScriptsFromFile(create_file, populate_file, connection):

    # get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user=getpass.getuser()

    # get password
    pw = getpass.getpass()

    # The URL we are connnecting to
    connStr = ''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'

    # Open and read the file as a single buffer
    fd1 = open(create_file, 'r')
    fd2 = open(populate_file, 'r')
    createFile1 = fd1.read()
    createFile2 = fd2.read()
    fd1.close()
    fd2.close()

    # all SQL commands (split on ';')
    createCommands = createFile1.split(';')
    populateCommands = createFile2.split(';')

    # initialize cursor
    curs = connection.cursor()

    try:
        #Execute each command 
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        for command in createCommands + populateCommands:
            if command not in ['', '\n']:
                try:
                    curs.execute(command)
                except cx_Oracle.DatabaseError as exc:
                    print('***'+ command)
                    print("Command skipped: ", exc)

        connection.commit()                      

        rows = curs.execute('SELECT * FROM tickets')
        for row in rows:
            print(row)                      

        curs.close()
        connection.close()
    except OperationalError as  msg:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message) 

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

def showMainMenu(connection):
    # main screen, ask to login, register or exit
    while True:
        userStart = input("Login, Register or Exit? ")

        if (userStart == "login" or userStart == 'L'): 
            login.handleLogin(connection)
        elif (userStart == "register" or userStart == 'R'): 
            register.handleRegister(connection)
        elif (userStart == "exit" or userStart == 'E'):
            sys.exit("You have logged out of the program.")
        else: print ("Please select one of the options. \n")

def main():
    connection = startConnection()
    # TODO: take this out before submitting!!! this is solely for testing purposes
    executeScriptsFromFile('../res/prj_tables.sql', '../res/a2-data.sql', connection)                     
    showMainMenu(connection)

if __name__ == "__main__":
    main()
