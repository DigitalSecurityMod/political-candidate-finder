########## DEPRECATED: Replaced by app.py ##########
import requests
import json
from dotenv import load_dotenv
import os

#Construct URL for Google Civic API
def constructURL ():
    #Load environment variables from .env
    load_dotenv()
    API_KEY = os.getenv('GOOGLE_CIVIC_API_KEY')
    base_url = "https://www.googleapis.com/civicinfo/v2/representatives"
    url = f"{base_url}?key={API_KEY}"
    ZIP_CODE = '60622' #Example zip code
    url += f"&address={ZIP_CODE}"
    return url

#Check response from Google Civic API
def checkResponse (response):
    try:
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        if 'http' in str(e):
            e = str(e).split('?')
        else: 
            return None
        print(f"Error: Unable to fetch data from API {e[0]}")
        return False

#Gets the representative data for the given zip code
def getRepresentatives ():
    url = constructURL()
    response = requests.get(url) #send request to Google Civic API
    checkResponse(response)
    return response.json()

#Display the representative data
def displayRepresentatives (data):
    for official in data['officials']:
        name = official.get('name')
        if name == None:
            name = "Not Available"
        party = official.get('party')
        if party == None:
            party = "Not Available"
        print(f"Name: {name}, Party: {party}\n")

def main ():
    data = getRepresentatives()
    if data:
        displayRepresentatives(data)
    else:
        return None

if __name__ == "__main__":
    main()