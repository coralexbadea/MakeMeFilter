#!/usr/bin/env python
"""
This file will make a simple request to the Flask API for email processing.
""" 
import argparse
import requests

def main(email):

        # Define URL for Flask API endpoint.
        KERAS_REST_API_URL = "http://127.0.0.1:45000/predict"
        
        # Set the payload to JSON format.
        payload = {"email": email,}

        # Submit the request.
        r = requests.get(KERAS_REST_API_URL, json=payload)
 
        response = r.json()
        print(response)
        # Ensure the request was sucessful.
        #if response["success"]:
                # Loop over the predictions and display them.
         #       print(response['predictions'])

        # Otherwise, the request failed.
        #else:
         #       print("Request failed")
        return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Purple rain')
    parser.add_argument(
        '-e',
        dest='email',
        action='store',
        required=True,
        help="This is the email."
    )

    args = parser.parse_args()

    main(**vars(args))


