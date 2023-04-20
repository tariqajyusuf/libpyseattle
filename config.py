"""Constants and configuration variables in one place."""

# City of Seattle Utility Website, this is where you log in to see your account.
COS_UTILITY_USAGE_SITE = "https://myutilities.seattle.gov/eportal/#/usage"
COS_UTILITY_LOGIN_SUCCESS_TITLE = "City of Seattle Utility Services"
COS_UTILITY_LOGIN_TEXT = "Log In"
COS_CSV_SCHEMA = ["id", "address", "date", "consumption"]
COS_CSV_DATE_HEADER = COS_CSV_SCHEMA[2]
COS_CSV_CONSUMPTION_HEADER = COS_CSV_SCHEMA[3]
