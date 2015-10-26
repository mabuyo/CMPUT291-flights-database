import main
import queries2 as q
import util_methods as util

class UserMenu(object):
    def __init__(self, email):
        self.email = email
        self.bookings = []

    def showMenu(self):
        """
        This shows the user menu for searching flights, listing existing bookings or logging out.
        """
        while True:
            userInput = input("Search for flights (S) or List existing bookings (B), Logout (L)?  ")
            if (userInput == "S"):
                self.searchForFlights()
            elif (userInput == "B"):
                self.showExistingBookings()
                self.promptForBooking()
            elif (userInput == "L"):
                self.setLastLogin()
                main.showMainMenu()
            else: print("Pick a valid option. \n")
    
    #AnjuMenu
    def searchForFlights(self, acode_s=None, acode_d=None, date=None):
        """
        This menu is for searching for flights.
        """
        if not acode_s: acode_s = ""
        if not acode_d: acode_d = ""
        if not date: date = ""
        while set([acode_s, acode_d, date]).intersection([""]):
            if acode_s == "":
                src = input("Enter the source airport ('R' for previous menu): ")
                if src == 'R': self.showMenu()
                acode_s = self.getAcode(src) 
            
            if acode_d == "":
                dst = input("Enter the destination airport ('R' to re-enter src): ")
                if dst == 'R': self.searchForFlights(acode_s=acode_s)
                acode_d = self.getAcode(dst) 

            if date == "":
                date = input("Enter the date of travel in format DD/MM/YYYY ('R' to re-enter dst): ")
                if dst == 'R': self.searchForFlights(acode_s=acode_s, acode_d=acode_d)
                if not util.validate(date):
                    date = input("Try again ('R' for previous menu): ")
        
        flights = q.searchFlights(acode_s, acode_d, date)
        if flights:
            print ("Here are flights that match your query: ")
            for f in flights:
                print(f[0], f[1], f[2], f[3], str(f[4]), str(f[5]), f[6], f[7], f[10], f[11])
            self.bookingOptions(flights, acode_s, acode_d, date)
        else: 
            print("No flights found, Try again.")
             
        
    #AnjuMenu
    def bookingOptions(self, searchResults, acode_s, acode_d, date):
        # get trip type
        print("\n")      
        tripType = input("Book one-way trip (1) or book round-trip (2).\n")
        if tripType == "1":
            rowSelection = input("Please enter row number of trip you would like to book.\n")
            try:
                self.bookings(searchResults[rowSelection])
            except:
                print("Could not complete booking. Please try again.\n")
                self.showMenu()        
        elif tripType == "2":
            return_date = input("Please enter return date in format DD/MM/YYYY.\n")
            if not util.validate(return_date): # date is invalid. let's you try twice, then shows you the list of availble flights
                return_date = input("Please enter return date in format DD/MM/YYYY.\n")

            returnFlights = q.searchFlights(acode_d, acode_s, return_date) # search for return flights
            if returnFlights:
                print ("Here are the return flights that match your query: ")
                for f in returnFlights:
                    print(f[0], f[1], f[2], f[3], str(f[4]), str(f[5]), f[6], f[7], f[10], f[11])
                rowSelectionDepart = input("Please enter row number of departure flight from first table.\n")
                rowSelectionReturn = input("Please enter row number of return flight from second table.\n")
                try:
                    self.bookings(searchResults[rowSelectionDepart]) # departure flight
                    self.bookings(returnFlights[rowSelectionReturn]) # return flight
                except:
                    print("Could not complete booking. Please try again.\n")
            else: 
                print("No return flights found, Try again.")

        else: # did not pick 1 or 2
            self.bookingOptions(searchResults, acode_s, acode_d, date)


    # AnjuMenu
    def getAcode(self, airport):
        if airport == "R": self.showMenu()
        elif q.isValidAcode(airport):
            return airport.upper()
        else: 
            q.getMatchingAirports(airport); 
            acode = input("Please select a 3-letter airport code from the list and enter it here: ")
            

    def showExistingBookings(self):
        """
        This shows the user's existing bookings.
        """
        searchBookings = "SELECT t.tno, p.name, TO_CHAR(b.dep_date, 'DD-MON-YYYY') as dep_date , t.paid_price FROM users u, passengers p, tickets t, bookings b WHERE u.email = p.email AND p.email = t.email AND t.tno = b.tno AND u.email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(searchBookings)
        booking_results = db.cursor.fetchall()
        if len(booking_results) == 0:
            print("No existing bookings found.")
            self.showMenu()
        print ("Ticket #    Name    Departure Date      Price\n")
        self.bookings = []
        for result in booking_results:
            self.bookings.append(result[0])
            print (str(result[0]) + "    " + result[1] + "   " + str(result[2]) + "   " + str(result[3]) + "\n")

    def promptForBooking(self):
        """
        This prompts the user to enter a ticket number out of the existing bookings or return to the previous menu.
        """
        while True:
            ticket_no = input("Enter your ticket number for more details about that booking. R to return to previous menu. \n")
            if ticket_no == "R": self.showMenu()
            if int(ticket_no) in self.bookings:
                showDetails = "SELECT tno, flightno, fare, dep_date, seat FROM bookings WHERE tno = " + ticket_no
                db = main.getDatabase()
                db.execute(showDetails)
                details = db.cursor.fetchall()
                for d in details: print(d)  
                self.detailedBooking(ticket_no)
            else: print("Please enter a valid ticket number. ")

    def detailedBooking(self, tno):
        """
        The details of the booking have been shown, the user can cancel the booking or return to their list of existing bookings. 
        """
        while True:
            action = input("Cancel this booking (C) or Return to list of existing bookings (R): ")
            if action == "C": 
                self.cancelBooking(tno)
            elif action == "R":
                self.showExistingBookings()
                self.promptForBooking()
            else: print("Please enter a valid input. ")

    def makeABooking():
        pass

    def cancelBooking(self, tno):
        dBook = "DELETE FROM bookings WHERE tno = " + tno;
        dTix = "DELETE FROM tickets WHERE tno = " + tno;
        db = main.getDatabase()
        db.execute(dBook)
        db.execute(dTix)
        db.execute("commit")
        print("Booking successfully cancelled. Returning to main menu.\n")
        self.showMenu()

    def setLastLogin(self):
        logout = "UPDATE users SET last_login = SYSDATE " + "WHERE email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(logout)
        db.execute("commit")
        print("Successfully logged out.\n")



