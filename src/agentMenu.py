import userMenu
import main

class AgentMenu(userMenu.UserMenu):
    """
    AgentMenu inherits from UserMenu with added functionality of recording an actual departure and actual arrival time.
    """
    def __init__(self, email):
        super().__init__(email)

    def showMenu(self):
        # user menu plus more
        while True:
            userInput = input("Search for flights (S) or List existing bookings (B), Logout (L)?  ")
            if (userInput == "S"):
                m = input("Would you like to search for multiple passengers? (y/n): ")
                if m == 'y' or m == 'Yes' or m =='yes':
                    self.promptAndSearchForFlights(True)
                else:
                    self.promptAndSearchForFlights()
            elif (userInput == "B"):
                self.showExistingBookings()
                self.promptForBooking()
            elif (userInput == "RD"):
                print("Recording flight departure. ")
                (fno, date) = self.findFlight()
                update = self.promptUpdate()
                self.recordDep(fno, date, update)
            elif (userInput == "RA"):
                print("Recording flight arrival. ")
                (fno, date) = self.findFlight()
                update = self.promptUpdate()
                self.recordArr(fno, date, update)
            elif (userInput == "L"):
                self.setLastLogin()
                main.showMainMenu()
            else: 
                print("Pick a valid option. \n")

    def findFlight(self):
        while True:
            flight = input("Enter the flight number and departure date (DD-MON-YYYY), separated using a space. (R) to return.  ")
            if flight == 'R': self.showMenu()
            (fno, date) = flight.split(" ")

            # check if flight exists
            checkValidFlight = "SELECT * FROM sch_flights WHERE flightno = '" + fno + "' AND dep_date = TO_DATE('" + date + "', 'DD-MON-YYYY')"
            db = main.getDatabase()
            db.execute(checkValidFlight)
            found = db.cursor.fetchall()
            if len(found) > 0: return (fno, date)
            else: print("\nNo flights found, try again.\n")

    def promptUpdate(self):
        while True:
            date = input("Record the actual time (DD-MON-YYY, HH:MI): ")
            if date == 'R': self.showMenu()
            return date

    def recordDep(self, fno, date, update):
        record = "UPDATE sch_flights SET act_dep_time = TO_DATE('" + update + "', 'DD-MON-YYYY, hh24:mi') WHERE (flightno = '" + fno +  "' AND dep_date = TO_DATE('" + date + "', 'DD-MON-YYYY'))"
        db = main.getDatabase()
        db.execute(record)
        db.execute("commit")
        print("Successfully recorded actual departure time.")
        self.showMenu()

    def recordArr(self, fno, date, update):
        record = "UPDATE sch_flights SET act_arr_time = TO_DATE('" + update + "', 'DD-MON-YYYY, hh24:mi') WHERE (flightno = '" + fno +  "' AND dep_date = TO_DATE('" + date + "', 'DD-MON-YYYY'))"
        db = main.getDatabase()
        db.execute(record)
        db.execute("commit")
        print("Successfully recorded actual arrival time.")
        self.showMenu()
