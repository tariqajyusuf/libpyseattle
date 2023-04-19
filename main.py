import scl
from getpass import getpass

print("Please log in to your City of Seattle Account")
username = str(input("Username: "))
password = str(getpass("Password: "))

scl = scl.SeattleCityLight()
print(scl.GetUsage(username, password))
