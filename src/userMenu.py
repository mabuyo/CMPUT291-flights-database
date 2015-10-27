from random import randint
import cx_Oracle
import sys

import searchFlights as sf
import util_methods as util
import main

BOOKING_QUERY = "SELECT t.tno, p.name, TO_CHAR(b.dep_date, 'DD-MON-YYYY') as dep_date , t.paid_price FROM users u, passengers p, tickets t, bookings b WHERE u.email = p.email AND p.email = t.email AND t.tno = b.tno AND u.email = '{0}' AND t.name = p.name AND t.email = p.email"

INSERT_PASSENGER = "INSERT INTO passengers VALUES('{0}', '{1}', '{2}')"
INSERT_TICKET = "INSERT INTO tickets VALUES('{0}', '{1}', '{2}', '{3}')"
INSERT_BOOKING = "INSERT INTO bookings VALUES('{0}', '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), '{4}')"

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
                m = input("Would you like to search for multiple passengers? (y/n): ")
                if m == 'y' or m == 'Yes' or m =='yes':
                    self.promptAndSearchForFlights(True)
                else:
                    self.promptAndSearchForFlights()
            elif (userInput == "B"):
                self.showExistingBookings()
                self.promptForBooking()
            elif (userInput == "L"):
                self.setLastLogin()
                main.showMainMenu()
            else: 
                print("Pick a valid option. \n")

    def promptForFlightDetails(self, acode_s=None, acode_d=None, date=None):
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
                if dst == 'R': self.promptForFlightDetails()
                acode_d = self.getAcode(dst) 

            if date == "":
                date = input("Enter the date of travel in format DD/MM/YYYY ('R' to re-enter dst): ")
                if dst == 'R': self.promptForFlightDetails(acode_s=acode_s)
                if not util.validate(date):
                    date = input("Invalid date. Try again ('R' for previous menu): ")
        return acode_s, acode_d, date        

    
    def promptNumPassengers(self):
        num = 0 
        while num==0:
            num = input("Input the number of passengers to search for: \n")
            try:
                num = int(num)
                return num 
            except ValueError:
                num = input("Please enter a valid number:  \n")

    def promptAndSearchForFlights(self, multiple_passengers=False):
        """
        This menu is used to search for flights.
        """
        if multiple_passengers == True:
            num = self.promptNumPassengers()
        else:
            num = 1 
        acode_s, acode_d, date = self.promptForFlightDetails()
        flights = sf.searchFlights(acode_s, acode_d, date, num, displayable=True)
        if flights:
            self.printFlightData(flights, mentionPriceSorted=False)
            print("")
            sort = input("This is currently sorted by price alone.\n"
                         "To sort by connections, and then price, enter 'C'.\n"
                         "('R' -> Main Menu; 'B' -> Book Flight): ")
            while True:
                if sort == 'P':
                    flights = sf.searchFlights(acode_s, acode_d, date, num, displayable=True)
                    if flights:
                        self.printFlightData(flights, mentionPriceSorted=True)
                        printFlightData("")
                        sort = input("This is currently sorted by price alone.\n"
                                     "To sort by connections, and then price, enter 'C'.\n"
                                     "('R' -> Main Menu; 'B' -> Book Flight): ")
                elif sort == 'C': 
                    flights = sf.searchFlightsSortedByConnections(acode_s, acode_d, date, num, displayable=True)
                    if flights:
                        self.printFlightData(flights, mentionConnectionSorted=True)
                        print("")
                        sort = input("This is currently sorted by connections, then price.\n"
                                     "To sort by price only, enter 'P'.\n"
                                     "('R' -> Main Menu; 'B' -> Book Flight): \n")
                elif sort == 'B':
                    flights = sf.searchFlights(acode_s, acode_d, date, num, displayable=False)
                    self.bookingOptions(flights, acode_s, acode_d, date, num)    # go to booking option
                elif sort == 'R':
                    self.showMenu()
                else: sort = input("Not a valid option. Please try again: \n ")
        else: 
            print("No flights found, Try again.")

    
    def printFlightData(self, flights, mentionPriceSorted=False, mentionConnectionSorted=False):
        if mentionPriceSorted:
            print ("Sorted by price: ")
        elif mentionConnectionSorted:
            print ("Sorted by connections: ")
        else: 
            print ("Here are flights that match your query: ")
        
        print("# flightno1  flightno2  SRC  DST  dep_time  arr_time  layover  numStops  price  seats ")
        i = 0
        for f in flights:
            i += 1
            print(i, f[0], f[1], f[2], f[3], str(f[4]), str(f[5]), f[6], f[7], f[8], f[9])
        
    
    def bookParties(self, searchResults, acode_s, acode_d, date):
        """
        For booking parties more than one passenger.
        """
        passengers = input("Please enter the number of passengers.\n")
            
        l = list(searchResults[int(float(rowSelection))])
        l.append(date)
        flightDetails = tuple(l)
        self.makeABooking(flightDetails) 

    def bookingOptions(self, searchResults, acode_s, acode_d, date, passengerCount=1):
        """
        For one-way trip and round trip options.
        """
        # get trip type
        print("")      
        if passengerCount == 1:
            tripType = input("Book one-way trip (1) or book round-trip (2): ")
        else:
            tripType = "1"
        if tripType == "1":
            rowSelection = input("Please enter row number of trip you would like to book: ")
            
            l = list(searchResults[int(float(rowSelection)) - 1])
            l.append(date)
            flightDetails = tuple(l)
            for i in range(passengerCount):
                self.makeABooking(flightDetails, passengerCount) 

        elif tripType == "2":
            return_date = input("Please enter return date in format DD/MM/YYYY.\n")
            if not util.validate(return_date): # date is invalid. let's you try twice, then shows you the list of availble flights
                return_date = input("Please enter return date in format DD/MM/YYYY.\n")

            returnFlights = sf.searchFlights(acode_d, acode_s, return_date) # search for return flights

            if returnFlights:
                print ("Here are the return flights that match your query: ")
                
                self.printFlightData(returnFlights); 
                rowSelectionDepart = input("Please enter row number of departure flight from first table: ")
                rowSelectionReturn = input("Please enter row number of return flight from second table: ")

                # add some more flight details to tuple
                twoBookings = []
                l = list(searchResults[int(float(rowSelectionDepart))-1])
                l.append(date)
                flightDetails = tuple(l)
                twoBookings.append(flightDetails)
                #self.makeABooking(flightDetails)    #departure flight
                print("Booking departure flight.\n")
                # add some more flight details to tuple
                l = list(returnFlights[int(float(rowSelectionReturn))-1])
                l.append(return_date)
                returnDetails = tuple(l)
                twoBookings.append(returnDetails)
                #self.makeABooking(returnDetails) # return flight
                self.makeABooking(twoBookings, passengerCount, True) # return flight

                print("Booking return flight.\n")

            else: 
                print("No return flights found, Try again.")

        else: # did not pick 1 or 2
            self.bookingOptions(searchResults, acode_s, acode_d, date)

    def getAcode(self, airport):
        if airport == "R": self.showMenu()
        elif sf.isValidAcode(airport):
            return airport.upper()
        else: 
            matching = sf.getMatchingAirports(airport); 
            while True:
                acode = input("Please select a valid 3-letter airport code from the list and enter it here: ")
                if acode == "R": self.showMenu()
                elif acode in matching: return acode


    def showExistingBookings(self):
        """
        This shows the user's existing bookings.
        """
        db = main.getDatabase()
        db.execute(BOOKING_QUERY.format(self.email))
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
            showDetails = "SELECT tno, flightno, fare, dep_date, seat FROM bookings WHERE tno = '" + ticket_no + "'"
            db = main.getDatabase()
            db.execute(showDetails)
            details = db.cursor.fetchall()
            if details:
                self.detailedBooking(ticket_no, details)
            else: print("Please enter a valid ticket number. ")

    def detailedBooking(self, tno, details):
        """
        The details of the booking have been shown, the user can cancel the booking or return to their list of existing bookings. 
        """
        print("The details for ticket no " + tno + " are: \n")

        # get headings, print details
        db = main.getDatabase()
        showDetails = "SELECT tno, flightno, fare, dep_date, seat FROM bookings WHERE tno = '" + tno  + "'"
        headings = db.cursor.description
        headingsStr = "( "
        for h in headings:
            headingsStr += str(h[0]) + ", "
        headingsStr = headingsStr.strip(", ")
        headingsStr += ' )'
        print(headingsStr) 
        for d in details: 
            print(d)  
        print('\n')
        while True:
            action = input("Cancel this booking (C) or Return to list of existing bookings (R): ")
            if action == "C": 
                self.cancelBooking(tno)
            elif action == "R":
                self.showExistingBookings()
                self.promptForBooking()
            else: print("Please enter a valid input. ")


    '''
    example booking:
    src: wrl
    dst: mls
    13/12/2015

    return
    mls--> wrl
    08/08/2015
    '''

    ''' example for connections sorting

    '''
    
    def makeABooking(self, fullFlightDetails, num=1, roundTrip=False, user_name="",  oneOfMany=False):
        if roundTrip == True:
            flightDetails = fullFlightDetails[0]
        else: flightDetails = fullFlightDetails

        print(flightDetails)
        # flightDetails: flightno1(0), flightno2(1), src(2), dst(3), dep_time(4), arr_time(5), layover(6), numStops(7), fare1(8), fare2(9), price(10), seats(11), dep_date(12)
        flightno, flightno2, src, dst, dep_time, arr_time, layover, numStops, fare1, fare2, price, seats, dep_date = flightDetails
        price = str(price)
        seat = self.generateSeatNumber()

        # get name of user, check if in passengers table
        if user_name == "": 
            user_name = input("Please enter your first and last name: ").title()
        checkIfPassenger = "SELECT * FROM passengers WHERE email = '{0}' and name = '{1}'".format(self.email, user_name)
        db = main.getDatabase()
        db.execute(checkIfPassenger)
        isPassenger = db.cursor.fetchall()

        if len(isPassenger) == 0:    # not in passengers table 
            country = self.promptForCountry()

            db.execute(INSERT_PASSENGER.format(self.email, user_name, country))
            db.execute("commit")
        else: 
            country = isPassenger[0][2]
            
        tno = str(self.generateTicketNumber())

        if oneOfMany:
            cheapSpecific = sf.getCheapestSpecificFlight(flightDetails)
        
        # check if seat is still available by searching for the flights again
        flights = sf.searchFlights(src, dst, dep_date, num)

        if len(flights) == 0:
            print("Sorry, this seat is no longer available. Please try another flight.")
            self.showMenu()

        else: 
            try: 
                db.execute(INSERT_TICKET.format(tno, user_name, self.email, price))
                db.execute(INSERT_BOOKING.format(tno, flightno, fare1, dep_date, seat))
                db.execute("commit")  
                tix = tno
                if (flightno2 != None):
                   tno2 = str(self.generateTicketNumber())
                   tix = tno + ", " + tno2
                   seat2 = self.generateSeatNumber()
                   db.execute(INSERT_TICKET.format(tno2, user_name, self.email, price))
                   db.execute(INSERT_BOOKING.format(tno2, flightno2, fare2, dep_date, seat))
                   db.execute("commit")
                print("Your flight has been booked with the ticket number(s): " + tix + ". \n")
                if (roundTrip == True): 
                    self.makeABooking(fullFlightDetails[1], num, False, user_name)  
            except cx_Oracle.DatabaseError as exc:
                error = exc.args
                print( sys.stderr, "Oracle code:", error.code)
                print( sys.stderr, "Oracle message:", error.message)
            self.showMenu()  

    def generateTicketNumber(self):
        """
        Generates a ticket number by getting the max ticket number from the tickets table and incrementing by one.
        """
        # get max tno
        findMaxTno = "SELECT MAX(tno) FROM tickets"
        db = main.getDatabase()
        db.execute(findMaxTno)
        maxTno = db.cursor.fetchall()
        if len(maxTno) == 0: return 1
        else: return int(maxTno[0][0]) + 1

    def generateSeatNumber(self):
        """
        Generates seat number by random and does not assign already taken seats, regardless of flightno (TA Kriti suggested this to avoid complications)
        """
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        assignedSeats = main.getAssignedSeats()
        letterIndex = randint(0, 25)
        letter = alphabet[letterIndex]
        num = randint(1,9)
        seat = letter + str(num)
        while (seat in assignedSeats):
            letterIndex = randint(1, 26)
            letter = alphabet[letterIndex+1]
            num = randint(1,9)
            seat = letter + str(num)
        return seat

    def cancelBooking(self, tno):
        """
        Cancels selected tno booking.
        """
        dBook = "DELETE FROM bookings WHERE tno = " + tno;
        dTix = "DELETE FROM tickets WHERE tno = " + tno;
        db = main.getDatabase()
        db.execute(dBook)
        db.execute(dTix)
        db.execute("commit")
        print("Booking successfully cancelled. Returning to main menu.\n")
        self.showMenu()

    def setLastLogin(self):
        """
        Logs out the user and updates last_login
        """
        logout = "UPDATE users SET last_login = SYSDATE " + "WHERE email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(logout)
        db.execute("commit")
        print("Successfully logged out.\n")

    def promptForCountry(self):
        """
        Used when user is not in the passengers table.
        """
        while True:
            country = input("Please enter your country: ")
            if len(country) > 0: return country    



