import userMenu
import agentMenu
import main

def handleUserMenu(email):
    menu = userMenu.UserMenu(email)
    menu.showMenu()


def handleAgentMenu(email):
    menu = agentMenu.AgentMenu(email)
    menu.showMenu()
