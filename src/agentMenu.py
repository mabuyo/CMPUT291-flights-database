import userMenu
import main

class AgentMenu(userMenu.UserMenu):
    def __init__(self, connection):
        super() 

    def showMenu(self):
        # user menu plus more
        # record a flight departure
        while True:
            userInput = input("Search for flights (S), List existing bookings (B), Record a flight departure (RD), Record a flight arrival (RA), Logout(L)?  ")
            if (userInput == "S"):
                print("Searching for flights")
            elif (userInput == "B"):
                print("Listing")
            elif (userInput == "RD"):
                print("Recording flight departure")
            elif (userInput == "RA"):
                print("Recording flight arrival")
            elif (userInput == "L"):
                main.showMainMenu(self.connection)
            else: print("Pick a valid option. \n")

        # record a flight arrival
        


