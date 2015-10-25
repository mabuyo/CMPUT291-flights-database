import main

TRIP_QUERY = ""


def getMatchingAirports(userInput):

    airport_query = "SELECT *  FROM airports WHERE name LIKE '%" + userInput + "%'" + " OR city LIKE '%" + userInput + "%'"  
    print(airport_query) 
    db = main.getDatabase()
    db.execute(airport_query) 
    airport_info = db.cursor.fetchall()
    
    for airport in airport_info: 
        print(airport) 

def searchFlights(src, dst, 

