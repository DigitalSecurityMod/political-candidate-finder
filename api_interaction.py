import requests
import json
from dotenv import load_dotenv
import os

#Load environment variables from .env
load_dotenv()

#Get API key
API_KEY = os.getenv('GOOGLE_CIVIC_API_KEY')
ZIP_CODE = '60622' #Example zip code

def constructURL ():
    base_url = "https://www.googleapis.com/civicinfo/v2/representatives"
    url = f"{base_url}?key={API_KEY}"
    if ZIP_CODE:
        url += f"&address={ZIP_CODE}"
    return url

def sendRequest (url):
    response = requests.get(url)
    return response

def checkResponse (response):
    try:
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError:
        return False

def parseResponse (response):
    data = response.json()

def printResponse (data):
    print(json.dumps(data, indent=4))

def main ():
    url = constructURL()
    response = sendRequest(url)
    if checkResponse(response):
        data = parseResponse(response)
        printResponse(data)
    else:
        print("Error: Unable to fetch data from API")
if __name__ == "__main__":
    main()