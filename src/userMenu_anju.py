import main
import searchFlights as sf
import util_methods as util
from random import randint

class UserMenu(object):
    def __init__(self, email):
        self.email = email
        self.bookings = []
        self.getUserDetails()

    def getUserDetails(self):
        """
        Gets name and country if user already exists in passengers.
        """
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

    
    def promptAndSearchForFlights(self, multiple_passengers=False):
        """
        This menu is used to search for flights.
        """
        if multiple_passengers:
            while num==0:
                num = input("Input the number of passengers to search for: \n")
                try:
                    num = int(num)
                except ValueError:
                    num = input("Please enter a valid number:  \n")
        else:
            num = 1; 

        acode_s, acode_d, date = self.promptForFlightDetails()
        flights = sf.searchFlights(acode_s, acode_d, date)
        if flights:
            self.printFlightData(flights, mentionPriceSorted=False)
            print("")
            sort = input("This is currently sorted by price alone.\n"
                         "To sort by connections, and then price, enter 'C'.\n"
                         "('R' -> Main Menu; 'B' -> Book Flight): ")
            while True:
                if sort == 'P':
                    flights = sf.searchFlights(acode_s, acode_d, date, num)
                    if flights:
                        self.printFlightData(flights, mentionPriceSorted=True)
                        print("")
                        sort = input("This is currently sorted by price alone.\n"
                                     "To sort by connections, and then price, enter 'C'.\n"
                                     "('R' -> Main Menu; 'B' -> Book Flight): ")
                elif sort == 'C': 
                    flights = sf.searchFlightsSortedByConnections(acode_s, acode_d, date, num)
                    if flights:
                        self.printFlightData(flights, mentionConnectionSorted=True)
                        print("")
                        sort = input("This is currently sorted by connections, then price.\n"
                                     "To sort by price only, enter 'P'.\n"
                                     "('R' -> Main Menu; 'B' -> Book Flight): \n")
                elif sort == 'B':
                    self.bookingOptions(flights, acode_s, acode_d, date)    # go to booking option
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
        
        print("flightno1  flightno2  SRC  DST  dep_time  arr_time  layover  numStops  price  seats ")
        for f in flights:
            print(f[0], f[1], f[2], f[3], str(f[4]), str(f[5]), f[6], f[7], f[10], f[11])
        
    
    def bookParties(self, searchResults, acode_s, acode_d, date):
        """
        For booking parties more than one passenger.
        """
        passengers = input("Please enter the number of passengers.\n")
            
        l = list(searchResults[int(float(rowSelection))])
        l.append(date)
        flightDetails = tuple(l)
        self.makeABooking(flightDetails) 

    def bookingOptions(self, searchResults, acode_s, acode_d, date):
        """
        For one-way trip and round trip options.
        """
        # get trip type
        print("\n")      
        tripType = input("Book one-way trip (1) or book round-trip (2).\n")
        if tripType == "1":
            rowSelection = input("Please enter row number of trip you would like to book.\n")
            
            l = list(searchResults[int(float(rowSelection))])
            l.append(date)
            flightDetails = tuple(l)
            self.makeABooking(flightDetails) 

        elif tripType == "2":
            return_date = input("Please enter return date in format DD/MM/YYYY.\n")
            if not util.validate(return_date): # date is invalid. let's you try twice, then shows you the list of availble flights
                return_date = input("Please enter return date in format DD/MM/YYYY.\n")

            returnFlights = sf.searchFlights(acode_d, acode_s, return_date) # search for return flights

            if returnFlights:
                print ("Here are the return flights that match your query: ")
                print("flightno1  flightno2  SRC  DST  dep_time  arr_time  layover  numStops  price  seats")
                for f in returnFlights:
                    print(f[0], f[1], f[2], f[3], str(f[4]), str(f[5]), f[6], f[7], f[10], f[11])
                rowSelectionDepart = input("Please enter row number of departure flight from first table.\n")
                rowSelectionReturn = input("Please enter row number of return flight from second table.\n")

                # add some more flight details to tuple
                l = list(searchResults[int(float(rowSelectionDepart))])
                l.append(date)
                flightDetails = tuple(l)
                self.makeABooking(flightDetails)    #departure flight

                # add some more flight details to tuple
                l = list(returnFlights[int(float(rowSelectionReturn))])
                l.append(date)
                returnDetails = tuple(l)
                self.makeABooking(returnDetails) # return flight
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
    
    def makeABooking(self, flightDetails):
        # flightDetails: flightno1(0), flightno2(1), src(2), dst(3), dep_time(4), arr_time(5), layover(6), numStops(7), fare1(8), fare2(9), price(10), seats(11), dep_date(12)       
        flightno = flightDetails[0]
        flightno2 = flightDetails[1] #will be 'None' if no connecting flight
        # numStops and layover will be zero if no connecting flight
        # TODO implement functionality for 
        src = flightDetails[2]
        dst = flightDetails[3]
        # dep_date is in format: datetime.datetime(2015, 12, 13, 13, 0)
        dep_date = flightDetails[12] 
        price = flightDetails[10]
        fare = flightDetails[8]
        fare2 = flightDetails[9]
        seat = self.generateSeatNumber()

        # get name of user, check if in passengers table
        checkIfPassenger = "SELECT * FROM passengers WHERE email = '" + self.email + "'"
        db = main.getDatabase()
        db.execute(checkIfPassenger)
        isPassenger = db.cursor.fetchall()

        if len(isPassenger) == 0:    # not in passengers table 
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

            # check if seat is still available by searching for the flights again
            flights = sf.searchFlights(src, dst, dep_date)

            if len(flights) == 0:
                print("Sorry, this seat is no longer available. Please try another flight.")
                self.showMenu()

            else: 
                insertTicket = "INSERT INTO tickets VALUES('" + tno + "', '" + name + "', '" + self.email + "', '" + str(price) + "')"
                insertBooking = "INSERT INTO bookings VALUES('" + tno + "', '" + flightno + "', '" + fare + "', to_date('" + dep_date + "', 'DD/MM/YYYY'), '" + seat + "')"
                
                try: 
                    db.execute(insertTicket)
                    db.execute("commit")  
                    db.execute(insertBooking)
                    db.execute("commit")  
                    if (flightno2 != None):
                        tno2 = self.generateTicketNumber()
                        tno2 = str(tno2)
                        seat2 = self.generateSeatNumber()
                        insertTicket2 = "INSERT INTO tickets VALUES('" + tno2 + "', '" + name + "', '" + self.email + "', '" + str(price) + "')"
                        insertBooking2 = "INSERT INTO bookings VALUES('" + tno + "', '" + flightno2 + "', '" + fare2 + "', to_date('" + dep_date + "', 'DD/MM/YYYY'), '" + seat + "')"
                        db.execute(insertTicket2)
                        db.execute("commit")  
                        db.execute(insertBooking2)
                        db.execute("commit")  
                        tix = tno + ", " + tno2
                    tix = tno
                    print("Your flight has been booked with the ticket number(s): " + tix + ". Returning to main menu...\n")
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
        #db.close()
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

    def promptForNameAndCountry(self):
        """
        Used when user is not in the passengers table.
        """
        while True:
            userInput = input("Please enter your name and country, separated by a space:  ")
            (name, country) = userInput.split(' ')
            if len(name) > 0 and len(country) > 0: return name, country
            else: print("Please enter valid input. \n")  



