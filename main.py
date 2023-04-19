"""A command line interface to access and download Seattle City Light usage."""

from getpass import getpass

import scl


def main():
    """Prompt for Seattle City Light login and print the last 30 days of consumption."""
    print("Please log in to your City of Seattle Account")
    username = str(input("Username: "))
    password = str(getpass("Password: "))

    utility = scl.SeattleCityLight()
    usage = utility.get_usage(username, password)
    print("Date\tkWh")
    for day, consumption in usage.items():
        print(f"{day}\t{consumption}")


if __name__ == '__main__':
    main()
