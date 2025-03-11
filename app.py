from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/representatives', methods=['POST'])
def api ():
    data = jsonify(get_representatives())
    return data

#Construct URL for Google Civic API
def construct_URL (api_key, zip_code):
    base_url = "https://www.googleapis.com/civicinfo/v2/representatives"
    url = f"{base_url}?key={api_key}"
    url += f"&address={zip_code}"
    return url

#Check response from Google Civic API
def check_response (response):
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
def get_representatives ():
    load_dotenv()
    API_KEY = os.getenv('GOOGLE_CIVIC_API_KEY')
    url = construct_URL(API_KEY, request.form('zipcode'))
    response = requests.get(url) #send request to Google Civic API
    check_response(response)
    return response.json()

##Display the representative data
#def displayRepresentatives (data):
#    for official in data['officials']:
#        name = official.get('name')
#        if name == None:
#            name = "Not Available"
#        party = official.get('party')
#        if party == None:
#            party = "Not Available"
#        print(f"Name: {name}, Party: {party}\n")


if __name__ == '__main__':
    app.run(debug=True)