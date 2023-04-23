"""A command line interface to access and download Seattle City Light usage."""

from getpass import getpass

from seattle import api
from seattle.citylight.usage import SeattleCityLight


def main():
    """Prompt for Seattle City Light login and print the last 30 days of consumption."""
    print("Please log in to your City of Seattle Account")
    seattle_api = api.API()
    utility = SeattleCityLight(seattle_api)
    while True:
        seattle_api.username = str(input("Username: "))
        seattle_api.password = str(getpass("Password: "))
        if seattle_api.get_authenticated():
            break

    usage = utility.get_recent_usage(window=1)
    print("Date\tkWh")
    for day, consumption in usage.items():
        print(f"{day}\t{consumption}")

    usage = utility.get_recent_usage(window=5)
    print("\n\nDate\tkWh")
    for day, consumption in usage.items():
        print(f"{day}\t{consumption}")


if __name__ == '__main__':
    main()
