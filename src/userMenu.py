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
                self.makeABooking(('AC1525', 'TWF','TSS', '19:35', '23:27', 0, 0, '189', 12, 'C', '06-Jul-2015'))
            else: 
                print("Pick a valid option. \n")
    
    '''
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
            
    '''

    
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
            
            print(searchResults[int(float(rowSelection))])
            try:
                self.makeABooking(searchResults[int(float(rowSelection))])
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
                    self.makeABooking(searchResults[int(float(rowSelectionDepart))]) # departure flight
                    self.makeABooking(returnFlights[int(float(rowSelectionReturn))]) # return flight
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


    '''
    example booking:
    src: wrl
    dst: mls
    13/12/2015

    return
    mls--> wrl
    08/08/2015
    '''
    
    def makeABooking(self, flightDetails):
        #flightDetails = (flight number, source, destination, departure time, arrival time, the number of stops, the layover time, the price, and the number of seats at that price, fare:notprinted, dep_date)
        # what is currently passed in: flightno1(0), flightno2(1), src(2), dst(3), dep_time(4), arr_time(5), layover(6), numStops(7), fare1(8), fare2(9), price(10), seats(11)        
        flightno = flightDetails[0]
        # flightno2 = flightDetails[1] will be 'None' if no connecting flight
        # numStops and layover will be zero if no connecting flight
        # TODO implement functionality for 
        src = flightDetails[2]
        dst = flightDetails[3]
        ####dep_date = flightDetails[10]  #### TODO will have to pass this in to the method, because it's not returned in the query
        price = flightDetails[10] # don't think this is needed for booking
        fare = flightDetails[8]
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
            # check if seat is still available by searching for the flights again
            FLIGHTS_AVAIL = "SELECT * FROM (select flightno1, flightno2, layover, price from ( select flightno1, flightno2, layover, price, row_number() over (order by price asc) rn from (select flightno1, flightno2, layover, price from good_connections where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}' union select flightno flightno1, '' flightno2, 0 layover, price from available_flights where to_char(dep_date,'DD/MM/YYYY')='{0}' and src='{1}' and dst='{2}'))) WHERE flightno1 = '" + flightno + "'"
            db.execute(FLIGHTS_AVAIL.format(dep_date, src, dst)) 
            flights = db.cursor.fetchall()
            if len(flights) == 0:
                print("Sorry, this seat is no longer available. Please try another flight.")
                self.showMenu()
            else: 
                insertTicket = "INSERT INTO tickets VALUES('" + tno + "', '" + name + "', '" + self.email + "', '" + price + "')"
                insertBooking = "INSERT INTO bookings VALUES('" + tno + "', '" + flightno + "', '" + fare + "', to_date('" + dep_date + "', 'DD-Mon-YYYY'), '" + seat + "')"
                try: 
                    db.execute(insertTicket)
                    db.execute("commit")  
                    db.execute(insertBooking)
                    db.execute("commit")  
                    print("Your flight has been booked with the ticket number " + tno + ". Returning to main menu...\n")
                except cx_Oracle.DatabaseError as exc:
                    error = exc.args
                    print( sys.stderr, "Oracle code:", error.code)
                    print( sys.stderr, "Oracle message:", error.message)
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



