import sys
import cx_Oracle
import getpass 
from sqlite3 import OperationalError

# project packages
import login
import register
import database

AVAILABLE_FLIGHTS = "create view available_flights(flightno,dep_date, src,dst,dep_time,arr_time,fare,seats, price) as select f.flightno, sf.dep_date, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.fare, fa.limit-count(tno), fa.price from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2 where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+) group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price having fa.limit-count(tno) > 0"

GOOD_CONNECTIONS_VIEW = "create view good_connections (src,dst,dep_date,flightno1,flightno2, layover,price, dep_time, arr_time, fare1, fare2, seats) as SELECT DISTINCT ff.src, ff.dst, ff.dep_date, ff.no1, ff.no2, ff.layover, ff.price, ff.dep_time, ff.arr_time, a3.fare, a4.fare, least(a3.seats, a4.seats)  FROM(select a1.src, a2.dst, a1.dep_date, a1.flightno AS no1, a2.flightno AS no2, a2.dep_time-a1.arr_time as layover, min(a1.price+a2.price) AS price, a1.dep_time, a2.arr_time, a2.dep_date as date2 from available_flights a1, available_flights a2 where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24>=a2.dep_time group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, a1.arr_time, a1.dep_time, a2.arr_time, a2.dep_date) ff, available_flights a3, available_flights a4 WHERE a3.dep_date = ff.dep_date and a3.flightno = ff.no1 AND a4.flightno = ff.no2 AND a4.dep_date = ff.date2 AND a3.dep_time = ff.dep_time AND a4.arr_time = ff.arr_time"

TEMP_CREATION = "CREATE TABLE temp (flightno1 CHAR(6), flightno2 CHAR(6), src CHAR(3), dst CHAR(3), dep_time DATE, arr_time DATE, layover NUMBER(38), numStops NUMBER(38), fare1 CHAR(2), fare2 CHAR(2), price NUMBER, seats NUMBER)"
CLEAR_SEARCH_RESULTS = "delete * FROM temp" 

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


        curs.execute("create table temp (flightno1 char(6), flightno2 char(6), src char(3), dst char(3), dep_time date, arr_time date, layover number(38), numstops number(38), fare1 char(2), fare2 char(2), price number, seats number)")
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
            db = getDatabase()
            db.cursor.close()
            db.close()  # close the connection when application is exited
            sys.exit("You have logged out of the program.")
        else: print ("Please select one of the options. \n")

def getDatabase():
    return db

def setup():
    """
    This is where any one-time setups go.
    """
    # read existing assigned seats from table
    # getAssignedSeats()
    db = getDatabase()
    
    try:
        db.execute(CLEAR_SEARCH_RESULTS)
        db.execute(TEMP_CREATION)
        db.execute("commit")
    except cx_Oracle.DatabaseError as e:
        pass 
    #db.execute("drop view available_flights")
    #db.execute(AVAILABLE_FLIGHTS)
    #db.execute("drop view good_connections")    
    #db.execute(GOOD_CONNECTIONS_VIEW)
    #db.execute(GOOD_CONNECTIONS_VIEW)
    db.execute("commit")

def getAssignedSeats():
    getSeats = "SELECT DISTINCT seat from bookings"
    db = getDatabase()
    db.execute(getSeats)
    seats = db.cursor.fetchall()
    assignedSeats = [s[0] for s in seats]
    return assignedSeats

def main():
    # TODO: take this out before submitting!!! this is solely for testing purposes
    # executeScriptsFromFile('../res/prj_tables.sql', '../res/a2-data.sql')                    
    setup()
    showMainMenu()


# database connection will be global    
db_input = getDatabaseDetails()
db = database.Database(db_input)


if __name__ == "__main__":
    main()
