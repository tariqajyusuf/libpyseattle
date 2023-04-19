"""A command line interface to access and download Seattle City Light usage."""

from getpass import getpass

import scl


def __main__():
    print("Please log in to your City of Seattle Account")
    username = str(input("Username: "))
    password = str(getpass("Password: "))

    utility = scl.SeattleCityLight()
    print(utility.get_usage(username, password))
