import main
def make_available_flights():
    
    db = main.getDatabase()
    db.execute(airport_query) 
