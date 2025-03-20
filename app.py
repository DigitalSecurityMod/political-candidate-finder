from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import json
import os
from requests.exceptions import HTTPError

#WARNING: Do not deploy to production with debug=True and CORS enabled
app = Flask(__name__)
CORS(app) #Cross-Origin Resource Sharing

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/representatives', methods=['POST'])
def api():
    zip_code = request.form['zip_code']
    print(zip_code)
    
    response, error = get_representatives(zip_code)
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(response.json())

#Construct URL for Google Civic API
def construct_URL (api_key, zip_code):
    base_url = "https://www.googleapis.com/civicinfo/v2/representatives"
    url = f"{base_url}?key={api_key}&address={zip_code}"
    return url

#Check response from Google Civic API
def check_response(response):
    try:
        response.raise_for_status()
        return True, None
    except HTTPError as e:
        response_json = json.loads(response.text)
        if 'error' in response_json and 'message' in response_json['error']:
            if response_json['error']['message'] == 'Failed to parse address':
                error_msg = "Error: Invalid Zip Code"
        elif 'http' in str(e):
            e_parts = str(e).split('?')
            error_msg = f"Error: Unable to fetch data from API {e_parts[0]}"
        else:
            error_msg = f"Error: {e}"
        
        print(error_msg)
        return False, error_msg

#Gets the representative data for the given zip code
def get_representatives(zip_code):
    load_dotenv()
    API_KEY = os.getenv('GOOGLE_CIVIC_API_KEY')
    if API_KEY == None:
        return None, "Error: Unable to fetch API Key"
    
    url = construct_URL(API_KEY, zip_code)
    response = requests.request("GET", url) #send request to Google Civic API
    success, error_message = check_response(response)
    if not success:
        return None, error_message
    
    return response, None