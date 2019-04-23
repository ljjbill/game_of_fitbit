#################################################
# IMPORT DEPENDENCIES FOR FLASK
#################################################
from flask import (
   Flask,
   render_template,
   jsonify,
   redirect,
   make_response,
   request)
from flask_cors import CORS

#################################################
# IMPORT DEPENDENCIES TO ACCESS DB THROUGH SQLALCHEMY FOR DATA INGRESS
#################################################
"""
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import (
   create_engine,
   func,
   inspect,
   extract)

from flask_sqlalchemy import SQLAlchemy
"""
#################################################
# IMPORT DEPENDENCIES FOR OTHER CODE WITHIN ROUTES
#################################################
from pandas.util import hash_pandas_object
import pandas as pd
import json
import requests
import datetime
from datetime import timedelta

#################################################
# IMPORT DEPENDENCIES FOR Machine Learning
#################################################
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from scipy import stats
import numpy as np
import xgboost as xgb
import math

#################################################
# Flask Setup
#################################################
app = Flask (__name__)
CORS(app)


# Database connection
"""
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///db/vital.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(db.engine, reflect=True)
"""

# Save references to each table
"""study = Base.classes.study""" # EXAMPLE

def xgboost_model(model_name, features):
    # model_name: name of the trained xgboost model, e.g.: 'calorie_predictor.model'
    # features: 1 x 11 features as numpy array, e.g.: np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]) where the numbers are feature values

    # Loads the model saved in model_name. Runs the model using given feature vector. Returns the predicted calories.

    # loading model
    mod = xgb.Booster({'nthread':4})
    mod.load_model(model_name)

    assert np.shape(features)[0] == 11 # make sure number of features is correct

    features = features[np.newaxis, :]
    feat = xgb.DMatrix(features)

    return mod.predict(feat)

def svm_model(model_name, scale_name, features):
    # model_name: name of the trained Gradient Boosted Regressor model, e.g.: 'calorie_predictor_GBR.model'
    # scale_name: name of file containing variable to scale features
    # features: 1 x 11 features as numpy array, e.g.: np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]) where the numbers are feature values

    # Loads the model saved in model_name. Runs the model using given feature vector. Returns the predicted calories.

    # loading model
    with open(model_name, 'rb') as f:
        calorie_model = pickle.load(f)

    # loading scaler
    with open(scale_name, 'rb') as f:
        X_scaler = pickle.load(f)

    assert np.shape(features)[0] == 11 # make sure number of features is correct

    features = features[np.newaxis, :]
    features = X_scaler.transform(features)


    return calorie_model.predict(features)


# creates a route for the flask front end
@app.route('/')
def home():
   """Return the homepage"""
   return render_template('index.html')

@app.route('/form')
def open_form():
   """go to form page"""
   return render_template('form.html')

@app.route('/test')
def open_test():
   """go to form page"""
   return render_template('Untitled.html')

def unpack_data(d):
   cols_list = ['list', 'of', 'col', 'names']
   return np.array([float(d[x][0]) for x in cols_list])

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        steps = request.form["userSteps"]
        tra_dist = request.form["TrackerDistance"]
        log_act_dist = request.form["LogActDist"]
        very_act_dist = request.form["VeryActDist"]
        mod_act_dist = request.form["ModActDist"]
        light_act_dist = request.form["LightActDist"]
        seden_act_dist = request.form["SedenActDist"]
        very_act_min = request.form["VeryActMin"]
        fair_act_min = request.form["FairActMin"]
        light_act_min = request.form["LightActMin"]
        seden_act_min = request.form["SedenMin"]
        print(request.form.get("chosenModel", None))
        d=request.form.to_dict(flat=False)
        try:
         #   if request.form.get("chosenModel", None) = "Model 1"

         #TODO: Refactor into a functions
         results = np.array([
            float(steps),
            float(tra_dist),
            float(log_act_dist),
            float(very_act_dist),
            float(mod_act_dist),
            float(light_act_dist),
            float(seden_act_dist),
            float(very_act_min),
            float(fair_act_min),
            float(light_act_min),
            float(seden_act_min)
            ])
         model_name = 'calorie_predictor.model'
         pred_calories = xgboost_model(model_name,results)
         # output = '{}'.format(pred_calories)
         output = round(pred_calories[0],2)
        except:
           output = 'Error: incorrect input!'

        return render_template("form.html", output=output)
# 

if __name__ == "__main__":
    app.run(debug = True)