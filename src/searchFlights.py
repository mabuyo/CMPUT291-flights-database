import main
import pprint
import cx_Oracle

CLEAR_SEARCH_RESULTS = "delete FROM temp" 

TRIP_QUERY_PARTIES = "INSERT into temp (flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats) select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats from ( select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, row_number() over (order by price asc) rn from (select flightno1, flightno2, src, dst, dep_time, arr_time, layover, 1 numStops, fare1, fare2, price, seats from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno, '' flightno2, src, dst, dep_time, arr_time, 0  layover, 0 numStops, fare, '' fare2, price, seats from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}') order by price)"

TRIP_QUERY_SORT_CONNECTIONS_PARTIES = "select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats from ( select flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, row_number() over (order by numStops asc, price asc) rn from (select flightno1, flightno2, src, dst, dep_time, arr_time, layover, 1 numStops, fare1, fare2, price, seats from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno, '' flightno2, src, dst, dep_time, arr_time, 0  layover, 0 numStops, fare, '' fare2, price, seats from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}') where seats >= {3} order by numStops asc, price asc)"

airport_query = "SELECT *  FROM airports WHERE name LIKE '%{0}%' OR city LIKE '%{0}%'"  

CHEAPEST_SPECIFC_FLIGHT = "SELECT * FROM (SELECT * FROM temp WHERE flightno1='{0}' AND flightno2 {1} AND dep_time = to_date('{2}', 'YYYY-MM-DD HH24:MI:SS') ORDER BY price) WHERE rownum = 1"

DISPLAYABLE = "SELECT flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, price, sum(seats) FROM temp GROUP BY  flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, price ORDER BY price ASC"
DISPLAYABLE_C = "SELECT flightno1, flightno2, src, dst, dep_time, arr_time  , layover, numStops, price, sum(seats) FROM temp GROUP BY  flightno1, flightno2, src, dst, dep_time, arr_time, layover, numStops, price ORDER BY numStops ASC, price asc"

def isValidAcode(code):
    """
    Checks to see if given airport code is valid by query to database.
    """
    db = main.getDatabase()
    db.execute('SELECT acode FROM airports') 
    return code.upper() in [code for result in db.cursor.fetchall() for code in result]

def getMatchingAirports(userInput):
    """
    userInput is taken as text to partial match from airport names and/or airport cities. A list of airports that match (partial) the given input is returned.
    """
    airport_query = "SELECT *  FROM airports WHERE name LIKE '%{0}%' OR city LIKE '%{0}%'"  
    db = main.getDatabase()
    db.execute(airport_query.format(userInput.title())) 
    airport_info = db.cursor.fetchall()
    while not airport_info:
        userInput = input("No airports found. Try entering the city or the name of the airport: ")
        db.execute(airport_query.format(userInput.title())) 
        airport_info = db.cursor.fetchall()
    print("")
    print("Here are existing airports that matched your query: \n")
    for airport in airport_info: 
        print(airport) 
    return [airportCode[0] for airportCode in airport_info]


def searchFlights(src, dst, dep_date, groupSize=1, displayable=False):
    """
    The main query for obtaining the flights available.
    displayable is an atrribute for more easily displaying the data in a readable format as per the specification. When set to False, it returns everything from the temp table. Clearing the temp table is important before re-populating it.
    """
    db = main.getDatabase()   
    db.execute(CLEAR_SEARCH_RESULTS)
    db.execute(TRIP_QUERY_PARTIES.format(dep_date, src, dst)) 
    if displayable: 
        db.execute(DISPLAYABLE) 
    else:
        db.execute("SELECT * FROM temp ORDER BY PRICE asc") 
    return db.cursor.fetchall()


def searchFlightsSortedByConnections(src, dst, dep_date, groupSize=1, displayable=False):
    # sort by number of connections and price
    db = main.getDatabase()   
    db.execute(TRIP_QUERY_SORT_CONNECTIONS_PARTIES.format(dep_date, src, dst, groupSize)) 
    if displayable: 
        db.execute(DISPLAYABLE_C) 
    else:
        db.execute("SELECT * FROM temp ORDER BY numstops asc, price asc") 
    return db.cursor.fetchall()

def getCheapestSpecificFlight(flightDetails):
    """
    For the implementation of booking for parties larger than one, as per the specifications.
    """
    flightno, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, dep_date = flightDetails
    db = main.getDatabase()   

    if flightno2 == None: flightno2 = "IS NULL"
    else: flightno2 = "= '" + flightno2 + "'"
    
    db.execute(CHEAPEST_SPECIFC_FLIGHT.format(flightno, flightno2, dep_time)) 

    cheap_flights = db.cursor.fetchall() 

    return cheap_flights
