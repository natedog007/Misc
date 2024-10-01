# Nathan Boyden
# Currency Converter using the Free Currency API

import requests

# API key used authenticating the program
API_KEY = ''
# Gives access to the actual converter
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}"

# Defines a list of currencies for conversion
CURRENCIES = ["USD", "CAD", "EUR", "AUD", "CNY"]


def convert_currency(base):
    # Combines all separate string with a comma in between each for the website to understand
    currencies = ",".join(CURRENCIES)

    # Creates an object that is basically a customizable url to the API's website.
    # It has the BASE_URL which just is the website, the base which is the current currency before conversion
    # and the CURRENCIES which just defines what currency the user wants to convert to
    url = f"{BASE_URL}&base_currency={base}&currencies={currencies}"

    # Attempts to run this string of code
    try:
        response = requests.get(url)
        data = response.json()
        return data["data"]

    # If it cannot it just prints an error and return nothing
    except Exception as e:
        print(e)
        return None


while True:

    # Asks user for base currency and forces answer to be upper case to match the array
    base = input("Enter base currency (Press 'q' if you want to quit the program): ").upper()

    if base == "Q":
        break

    data = convert_currency(base)
    # If data variable has no value skips deletion step and goes to the previous error catching step
    if not data:
        continue

    # Removes the specific currency selected by user
    del data[base]

    # Iterates through the array using the items() function to separate both the ticker and value
    # To be more easily printed
    for ticker, value in data.items():
        print(f"{ticker}: {value}")
