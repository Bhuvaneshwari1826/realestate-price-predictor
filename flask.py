import numpy as np
import pickle
import joblib
import matplotlib
import matplotlib.pyplot as plt
import time
import pandas
import os
from flask import Flask, request, jsonify, render_template
import json

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<your API_KEY>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8e16b491-9bb5-40c2-9ded-a3094b4de776/predictions?version=2021-11-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())


app = Flask(__name__)

#scale = pickle.load(open('C:/Users/SmartbridgePC/Desktop/AIML/Guided projects/rainfall_prediction/IBM end point deploy/scale.pkl','rb'))
@app.route('/') # rendering the html template
def home():
    return render_template('index.html')
@app.route('/predict') # rendering the html template
def predict() :
    return render_template("form1.html")
@app.route('/login') # rendering the html template
def login() :
    return render_template("login.html")
@app.route('/register') # rendering the html template
def register() :
    return render_template("register.html")

@app.route('/submit',methods=["POST","GET"])# route to show the predictions in a web UI
def submit():
    #  reading the inputs given by the user
    Area = request.form["Area"]
    City = request.form["City"]
    Bedrooms = request.form["No. of Bedrooms"]
    Resale = request.form["Resale"]
    Security = request.form["24X7Security"]
    CarParking = request.form["CarParking"]
    School = request.form["School"]
    Hospital = request.form["Hospital"]
    
    t = [[int(Area),int(City),int(Bedrooms),int(Resale),
          
          int(Security),int(CarParking),int(School),int(Hospital)]]
    payload_scoring = {"input_data": [{"field": [['Area', 'City', 'No. of Bedrooms', 'Resale', '24X7Security',
       'CarParking', 'School', 'Hospital']], "values": t}]}
    # add fields of ur dataset in above 2D list

    response_scoring = requests.post('<your scoring-end-point-url>', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    print(pred)
    return render_template('form1.html', prediction_text = pred)
    
     # showing the prediction results in a UI
if __name__=="__main__":
    
    # app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)
