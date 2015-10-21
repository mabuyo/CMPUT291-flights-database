import main

class UserMenu(object):
    def __init__(self, connection):
        self.connection = connection

    def showMenu(self):
        while True:
            userInput = input("Search for flights (S) or List existing bookings (B), Logout (L)?  ")
            if (userInput == "S"):
                print("Searching for flights")
            elif (userInput == "B"):
                print("Listing")
            elif (userInput == "L"):
                main.showMainMenu(self.connection)
            else: print("Pick a valid option. \n")

    def searchForFlights():
        while True:
            flightParameters = input("Enter the source, destination and departure date (DD-MON-YYYY), separated by spaces.")
        pass

    def showExistingBookings():
        pass

    def makeABooking():
        pass

    def deleteBooking():
        pass


