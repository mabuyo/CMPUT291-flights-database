import main
import pprint

TRIP_QUERY = "select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats from ( select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, row_number() over (order by price asc) rn from (select flightno1, flightno2, src, dst, dep_time, arr_time, layover, 1 numStops, fare1, fare2, price, seats from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno, '' flightno2, src, dst, dep_time, arr_time, 0  layover, 0 numStops, fare, '' fare2, price, seats from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}') order by price)"

TRIP_QUERY_SORT_CONNECTIONS = "select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats from ( select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, row_number() over (order by numStops asc, price asc) rn from (select flightno1, flightno2, src, dst, dep_time, arr_time, layover, 1 numStops, fare1, fare2, price, seats from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno, '' flightno2, src, dst, dep_time, arr_time, 0  layover, 0 numStops, fare, '' fare2, price, seats from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}') order by numStops asc, price asc)"

TRIP_QUERY_PARTIES = "select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats from ( select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, row_number() over (order by price asc) rn from (select flightno1, flightno2, src, dst, dep_time, arr_time, layover, 1 numStops, fare1, fare2, price, seats from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno, '' flightno2, src, dst, dep_time, arr_time, 0  layover, 0 numStops, fare, '' fare2, price, seats from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}') order by price) where seats >= '{3}'"

TRIP_QUERY_SORT_CONNECTIONS_PARTIES = "select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats from ( select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, row_number() over (order by numStops asc, price asc) rn from (select flightno1, flightno2, src, dst, dep_time, arr_time, layover, 1 numStops, fare1, fare2, price, seats from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno, '' flightno2, src, dst, dep_time, arr_time, 0  layover, 0 numStops, fare, '' fare2, price, seats from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}') where seats >= '{3}' order by numStops asc, price asc)"

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
    return [airportCode[0] for airportCode in airport_info]


#ef searchFlights(src, dst, dep_date):
#ensure that the src, dest and dep_date are in the correct format BEFORE calling this method
#   db = main.getDatabase()   
#   db.execute(TRIP_QUERY.format(dep_date, src, dst)) 
#   return db.cursor.fetchall()

#ef sortFlights(src, dst, dep_date):
#   # sort by number of connections and price
#   db = main.getDatabase()   
#   db.execute(TRIP_QUERY_SORT_CONNECTIONS.format(dep_date, src, dst)) 
#   return db.cursor.fetchall()

def searchFlights(src, dst, dep_date, groupSize=1):
    db = main.getDatabase()   
    db.execute(TRIP_QUERY_PARTIES.format(dep_date, src, dst, groupSize)) 
    return db.cursor.fetchall()

def searchFlightsSortedByConnections(src, dst, dep_date, groupSize=1):
    # sort by number of connections and price
    db = main.getDatabase()   
    db.execute(TRIP_QUERY_SORT_CONNECTIONS_PARTIES.format(dep_date, src, dst, groupSize)) 
    return db.cursor.fetchall()
