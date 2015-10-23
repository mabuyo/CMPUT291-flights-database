import main

class UserMenu(object):
    def __init__(self, email):
        self.email = email

    def showMenu(self):
        while True:
            userInput = input("Search for flights (S) or List existing bookings (B), Logout (L)?  ")
            if (userInput == "S"):
                self.searchForFlights()
            elif (userInput == "B"):
                self.showExistingBookings()
            elif (userInput == "L"):
                main.showMainMenu()
            else: print("Pick a valid option. \n")

    def searchForFlights(self):
        while True:
            flightParameters = input("Enter the source, destination and departure date (DD-MON-YYYY), separated by spaces.\n")
        pass

    def showExistingBookings(self):
        searchBookings = "SELECT t.tno, p.name, b.dep_date, t.paid_price FROM users u, passengers p, tickets t, bookings b WHERE u.email = p.email AND p.email = t.email AND t.tno = b.tno AND u.email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(searchBookings)
        booking_results = db.cursor.fetchall()
        for x in booking_results: print(x)

    def makeABooking():
        pass

    def deleteBooking():
        pass


