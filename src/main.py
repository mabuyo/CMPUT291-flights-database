import sys
import cx_Oracle
import getpass 
from sqlite3 import OperationalError

# project packages
import login
import register
import database
import queries2

def executeScriptsFromFile(create_file, populate_file):
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
    curs = db.cursor

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
                    print("Command skipped: ", exc)

        db.connection.commit()                      

        # example: rows = curs.execute('SELECT * FROM tickets')
        curs.close()
        db.connection.close()
    except OperationalError as  msg:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message) 

    print("Tables created and data successfully loaded.") 

def getDatabaseDetails():
    """
    Prompts user for SQL username and password to establish connection with the database.
    """
    # get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user=getpass.getuser()

    # get password
    pw = getpass.getpass()
    if not pw:
        pw = 'databases291'

    # The URL we are connnecting to
    connStr = ''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'

    return connStr

def showMainMenu():
    # main screen, ask to login, register or exit
    while True:
        userStart = input("Login (L), Register (R) or Exit (E)? ")

        if (userStart == "login" or userStart == 'L'): 
            login.handleLogin()
        elif (userStart == "register" or userStart == 'R'): 
            register.handleRegister()
        elif (userStart == "exit" or userStart == 'E'):
            sys.exit("You have logged out of the program.")
        else: print ("Please select one of the options. \n")

def getAssignedSeats():
    getSeats = "SELECT DISTINCT seat from bookings"
    db = getDatabase()
    db.execute(getSeats)
    seats = db.cursor.fetchall()
    assignedSeats = [s[0] for s in seats]
    return assignedSeats

def main():
    # TODO: take this out before submitting!!! this is solely for testing purposes
    #executeScriptsFromFile('../res/prj_tables.sql', '../res/a2-data.sql')  
    showMainMenu()

def getDatabase():
    return db

# database connection will be global    
db_input = getDatabaseDetails()
db = database.Database(db_input)


if __name__ == "__main__":
    main()
