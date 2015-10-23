import userMenu
import main

class AgentMenu(userMenu.UserMenu):
    def __init__(self, email):
        super().__init__(email)

    def showMenu(self):
        # user menu plus more
        # record a flight departure
        while True:
            userInput = input("Search for flights (S), List existing bookings (B), Record a flight departure (RD), Record a flight arrival (RA), Logout(L)?  ")
            if (userInput == "S"):
                self.searchForFlights()
            elif (userInput == "B"):
                self.showExistingBookings()
                self.promptForBooking()
            elif (userInput == "RD"):
                print("Recording flight departure.\n")
                (fno, date) = self.findFlight()
                update = self.promptUpdate()
                self.recordDep(fno, date, update)
            elif (userInput == "RA"):
                print("Recording flight arrival. \n")
                (fno, date) = self.findFlight()
                update = self.promptUpdate()
                self.recordArr(fno, date, update)
            elif (userInput == "L"):
                main.showMainMenu()
            else: print("Pick a valid option. \n")

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
            date = input("Record the actual departure time (DD-MON-YYY, HH:MI)")
            if date == 'R': self.showMenu()
            return date

    def recordDep(self, fno, date, update):
        # UPDATE sch_flights SET act_dep_time = TO_DATE(update, 'DD-MON-YYYY, HH:MI') WHERE flightno = input AND dep_date = TO_DATE(date,'DD-MON-YYYY')
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
