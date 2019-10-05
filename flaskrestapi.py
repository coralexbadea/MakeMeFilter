#!/usr/bin/env python
"""
This is the Flask REST API that processes and outputs the prediction on the email.
"""
import numpy as np
from keras.models import load_model
from keras.models import model_from_json
import tensorflow as tf
import flask
import json
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
import pickle
# Initialize our Flask application and the Keras model.
app = flask.Flask(__name__)


#load the pretrained model
with open('model_in_json.json','r') as f:
    model_json = json.load(f)

model = model_from_json(model_json)
model.load_weights('model.h5')


#load the pretrained CountVectorizer
vectorizer = pickle.load(open("vector.pickel", 'rb'))


global graph
graph = tf.get_default_graph()

def clean_review(text):
    #preprocessed the emails using reggex
    text = text.replace(r'^.+@[^\.].*\.[a-z]{2,}$', 'emailaddr')
    text = text.replace(r'^(http(s?)\:\/\/)*[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?', 'webaddr')
    text = text.replace(r"\(([0-9]{2}|0{1}((x|[0-9]){2}[0-9]{2}))\)\s*[0-9]{3,4}[- ]*[0-9]{4}", 'phonenum')
     # replane non-words/digits/spaces with a space
    text = text.replace(r'[^\w\d\s]', ' ')
 
    #replace multiple the blank spaces at the end of the email
    text = text.replace(r'\s+', ' ')
 
    
    text = text.replace(r'_', ' ') 
 
    return text


# Remove word stems using a Porter stemmer 
#keep only the root word



def prepare_email(email):

    ps = nltk.PorterStemmer()

    email = ' '.join(ps.stem(term) for term in email.split())

    #we have the stop words deleter imbeded in Count Vectorizer
    #It return a matrix of counter tokens having the max_features attr
    email= clean_review(email)
    email = [email]
  
    email_prepped = vectorizer.transform(email)
    
    return email_prepped

@app.route("/predict", methods=["GET"])
def predict():

    # Initialize the dictionary for the response.
    #data = {"success": False}

    # Check if POST request.
    if flask.request.method == "GET":
		
        # Grab and process the incoming json.
        incoming = flask.request.get_json()
        emails = []
        email = incoming["email"]
        email_from = incoming["from"]
       

        # Process and prepare the email.
        email_prepped = prepare_email(email)

        # classify the email and make the prediction.
        with graph.as_default():
            prediction = model.predict(email_prepped)
        print(prediction)
        data = {}
        data["predictions"] = []
        
        if prediction > 0.50:
            result = "email is probably spam."
        else:
            result = "email is probably not spam."
        
	# Processes prediction probability.
        prediction = float(prediction)
        prediction = prediction * 100
        
       
        r = {"result": result, "percentage": prediction, "from": email_from}
        data["predictions"].append(r)

        # Show that the request was a success.
        #data["success"] = True

    # Return the data as a JSON response.
    return flask.jsonify(data["predictions"])

# Start the server.
if __name__ == "__main__":
    print("Starting the server and loading the model...")
    app.run(host='0.0.0.0', port=45000)

