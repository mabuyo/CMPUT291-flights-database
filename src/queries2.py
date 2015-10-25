import main
import pprint

TRIP_QUERY = "select flightno1, flightno2, layover, price from ( select flightno1, flightno2, layover, price, row_number() over (order by price asc) rn from (select flightno1, flightno2, layover, price from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno flightno1, '' flightno2, 0 layover, price from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}'));"


def getMatchingAirports(userInput):

    airport_query = "SELECT *  FROM airports WHERE name LIKE '%" + userInput + "%'" + " OR city LIKE '%" + userInput + "%'"  
    print(airport_query) 
    db = main.getDatabase()
    db.execute(airport_query) 
    airport_info = db.cursor.fetchall()
    
    for airport in airport_info: 
        print(airport) 

def searchFlights(src, dst, dep_date):
#ensure that the src, dest and dep_date are in the correct format BEFORE calling this method
      

    TRIP_QUERY2 = "select flightno1, flightno2, layover, price from ( select flightno1, flightno2, layover, price, row_number() over (order by price asc) rn from (select flightno1, flightno2, layover, price from good_connections where to_char(dep_date,'DD/MM/YYYY')='" + dep_date + "' and src='" + src + "' and dst='" + dst + "'  union select flightno flightno1, '' flightno2, 0 layover, price from available_flights where to_char(dep_date,'DD/MM/YYYY')='" + dep_date + "' and src='" + src + "' and dst='" + dst + "'));"
    
    print(TRIP_QUERY.format(dep_date, src, dst))
    print(TRIP_QUERY2)
    db = main.getDatabase()
    db.execute(TRIP_QUERY2) 
    flights = db.cursor.fetchall()
    if flights:
        pprrint.pprint(flights)
