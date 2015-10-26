import main
import pprint

TRIP_QUERY = "select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats from ( select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, row_number() over (order by price asc) rn from (select flightno1, flightno2, src, dst, dep_time, arr_time, layover, 1 numStops, fare1, fare2, price, seats from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno, '' flightno2, src, dst, dep_time, arr_time, 0  layover, 0 numStops, fare, '' fare2, price, seats from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}') order by price)"

airport_query = "SELECT *  FROM airports WHERE name LIKE '%{0}%' OR city LIKE '%{0}%'"  

def isValidAcode(code):
    db = main.getDatabase()
    db.execute('SELECT acode FROM airports') 
    return code.upper() in [code for result in db.cursor.fetchall() for code in result]

def getMatchingAirports(userInput):

    airport_query = "SELECT *  FROM airports WHERE name LIKE '%{0}%' OR city LIKE '%{0}%'"  
    db = main.getDatabase()
    db.execute(airport_query.format(userInput.title())) 
    airport_info = db.cursor.fetchall()
    while not airport_info:
        userInput = input("No airports found. Please check search terms and try again: ")
        db.execute(airport_query.format(userInput.title())) 
        airport_info = db.cursor.fetchall()
    print("")
    print("Here are existing airports that matched your query: \n")
    for airport in airport_info: 
        print(airport) 

def searchFlights(src, dst, dep_date):
#ensure that the src, dest and dep_date are in the correct format BEFORE calling this method
      

    db = main.getDatabase()   
    #db.execute(GOOD_CONNECTIONS_VIEW)
    db.execute(TRIP_QUERY.format(dep_date, src, dst)) 
    return db.cursor.fetchall()

