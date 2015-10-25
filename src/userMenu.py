import main
import queries2 as q
import util_methods as util
from random import randint

class UserMenu(object):
    def __init__(self, email):
        self.email = email
        self.bookings = []
        self.getUserDetails()

    def getUserDetails(self):
        getDetails = "SELECT p.name, p.country FROM passengers p, users u WHERE p.email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(getDetails)
        details = db.cursor.fetchall()
        if len(details) > 0: 
            self.name = details[0][0]
            self.country = details[0][1]

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
            elif (userInput == "test"):
                #self.makeABooking(<flight details from flight results>)
                #insert into sch_flights values ('AC1525',to_date('06-Jul-2015','DD-Mon-YYYY'),to_date('19:35', 'hh24:mi'),to_date('23:27', 'hh24:mi'));
                #(flight number, source, destination, departure time, arrival time, the number of stops, the layover time, the price, and the number of seats at that price, fare:notprinted, dep_date)
                self.makeABooking(('AC1525', 'TWF','TSS', '19:35', '23:27', 0, 0, '189', 12, 'X', '06-Jul-2015'))
            else: print("Pick a valid option. \n")

    def searchForFlights(self):
        """
        This menu is for searching for flights.
        """
        acode_s, acode_d, date = "", "", ""
        while acode_s == "" and acode_d == "" and date == "":
            src = input("Enter the source airport ('R' for previous menu): ")
            acode_s = self.getAcode(src) 
            
            dst = input("Enter the destination airport ('R' for previous menu): ")
            acode_d = self.getAcode(dst) 

            date = input("Enter the date of travel in format DD/MM/YYYY ('R' for previous menu): ")
            if not util.validate(date):
                date = input("Try again ('R' for previous menu): ")
        
        q.searchFlights(acode_s, acode_d, date)

    def getAcode(self, airport):
        if airport == "R": self.showMenu()
        elif q.isValidAcode(airport):
            return airport
        else: 
            q.getMatchingAirports(airport); 
            acode = input("Please enter select a 3-letter airport code from the list and enter it here: ")
            

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
        #db.close()

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
                #db.close()
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

    def makeABooking(self, flightDetails):
        #flightDetails = (flight number, source, destination, departure time, arrival time, the number of stops, the layover time, the price, and the number of seats at that price, fare:notprinted, dep_date)
        flightno = flightDetails[0]
        dep_date = flightDetails[10]
        price = flightDetails[7]
        fare = flightDetails[9]
        seat = self.generateSeatNumber()

        # get name of user, check if in passengers table
        checkIfPassenger = "SELECT * FROM passengers WHERE email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(checkIfPassenger)
        isPassenger = db.cursor.fetchall()

        if len(isPassenger) < 0:    # not in passengers table 
            # ask for name and country
            (name, country) = self.promptForNameAndCountry()

            # add to passenger table
            addPassenger = "INSERT INTO passengers VALUES('" + self.email + "', '" + name + "', '" + country + "'"
            db.execute(addPassenger)
            db.execute("commit")
            #db.close()
        else: 
            # name and country already exists
            name = self.name
            country = self.country
            tno = self.generateTicketNumber()
            tno = str(tno)
            # check if seat is still available
            checkSeatsAvail = "SELECT limit FROM flight_fares WHERE flightno = '" + flightno + "' AND limit > 0"
            db.execute(checkSeatsAvail)
            seatAvail = db.cursor.fetchall()
            if len(seatAvail) < 0:
                print("Sorry, this seat is no longer available. Please try another flight.")
                self.showMenu()
            else: 
                insertTicket = "INSERT INTO tickets VALUES('" + tno + "', '" + name + "', '" + self.email + "', '" + price + "')"
                insertBooking = "INSERT INTO bookings VALUES('" + tno + "', '" + flightno + "', '" + fare + "', to_date('" + dep_date + "', 'DD-Mon-YYYY'), '" + seat + "')"
                db.execute(insertTicket)
                db.execute("commit")  
                db.execute(insertBooking)
                db.execute("commit")  
                print("Your flight has been booked with the ticket number " + tno + ". Returning to main menu...\n")
            self.showMenu()
        

    def generateTicketNumber(self):
        # get max tno
        findMaxTno = "SELECT MAX(tno) FROM tickets"
        db = main.getDatabase()
        db.execute(findMaxTno)
        maxTno = db.cursor.fetchall()
        if len(maxTno) < 0: return 1
        else: return int(maxTno[0][0]) + 1

    def generateSeatNumber(self):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        assignedSeats = main.getAssignedSeats()
        letterIndex = randint(1, 26)
        letter = alphabet[letterIndex+1]
        num = randint(1,9)
        seat = letter + str(num)
        while (seat in assignedSeats):
            letterIndex = randint(1, 26)
            letter = alphabet[letterIndex+1]
            num = randint(1,9)
            seat = letter + str(num)
        return seat

    def cancelBooking(self, tno):
        dBook = "DELETE FROM bookings WHERE tno = " + tno;
        dTix = "DELETE FROM tickets WHERE tno = " + tno;
        db = main.getDatabase()
        db.execute(dBook)
        db.execute(dTix)
        db.execute("commit")
        #db.close()
        print("Booking successfully cancelled. Returning to main menu.\n")
        self.showMenu()

    def setLastLogin(self):
        logout = "UPDATE users SET last_login = SYSDATE " + "WHERE email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(logout)
        db.execute("commit")
        #db.close()
        print("Successfully logged out.\n")

    def promptForNameAndCountry(self):
        while True:
            userInput = input("Please enter your name and country, separated by a space:  ")
            (name, country) = userInput.split(' ')
            if len(name) > 0 and len(country) > 0: return name, country
            else: print("Please enter valid input. \n")  



