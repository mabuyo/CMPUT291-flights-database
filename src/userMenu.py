import main

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

    def searchForFlights(self):
        """
        This menu is for searching for flights.
        """
        while True:
            flightParameters = input("Enter the source, destination and departure date (DD-MON-YYYY), separated by spaces. (R) for returning to previous menu.\n")
            if flightParameters == "R": self.showMenu()
            else: 
                print("To be implemented......\n")


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



