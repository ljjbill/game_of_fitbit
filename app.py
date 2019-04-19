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
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import (
   create_engine,
   func,
   inspect,
   extract)

from flask_sqlalchemy import SQLAlchemy

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
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///db/vital.sqlite"
db = SQLAlchemy(app)
"""
# reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(db.engine, reflect=True)
"""

# Save references to each table
"""study = Base.classes.study""" # EXAMPLE

def predict_calories(model_name, features):
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

# creates a route for the flask front end
@app.route('/')
def home():
   """Return the homepage"""
   return render_template('index.html')

@app.route('/form')
def open_form():
   """go to form page"""
   return render_template('form.html')

# class Vital(db.Model):
#     __tablename__ = 'vital'

#     id = db.Column(db.Integer, primary_key=True)
#     steps = db.Column(db.Integer)
#     tra_dist = db.Column(db.Integer)
#     log_act_dist = db.Column(db.Integer)
#     very_act_dist = db.Column(db.Integer)

#     def __repr__(self):
#         return '<Vital %r>' % (self.name)


# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     db.drop_all()
#     db.create_all()


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
        

      #   trace = {
      #   "steps": int(steps),
      #   "tra_dist": int(tra_dist),
      #   "log_act_dist": int(log_act_dist),
      #   "very_act_dist": int(very_act_dist),
      #   "mod_act_dist": int(mod_act_dist),
      #   "light_act_dist": int(light_act_dist),
      #   "seden_act_dist": int(seden_act_dist),
      #   "very_act_min": int(very_act_min),
      #   "fair_act_min": int(fair_act_min),
      #   "light_act_min": int(light_act_min),
      #   "seden_act_min": int(seden_act_min)
      #   }

      #   results = jsonify(trace)
        results = np.array([
           int(steps),
           int(tra_dist),
           int(log_act_dist),
           int(very_act_dist),
           int(mod_act_dist),
           int(light_act_dist),
           int(seden_act_dist),
           int(very_act_min),
           int(fair_act_min),
           int(light_act_min),
           int(seden_act_min)
           ])
        model_name = 'calorie_predictor.model'
        pred_calories = predict_calories(model_name,results)
        output = 'Predicted calories burned {}'.format(pred_calories)
        return jsonify(output)
      #   vital = Vital(steps=steps, tra_dist=tra_dist, log_act_dist=log_act_dist, very_act_dist=very_act_dist)
      #   db.session.add(vital)
      #   db.session.commit()
      #   return redirect("/api/vitals", code=302)

   #  return render_template("form.html")


# create route that returns data for plotting
# @app.route("/api/vitals")
# def pals():
   

#     results = db.session.query(Vital.steps,Vital.tra_dist,Vital.log_act_dist, Vital.very_act_dist).first()

#     steps = results[0]
#     tra_dist = results[1]
#     log_act_dist = results[2]
#     very_act_dist = results[3]

#     trace = {
#         "steps": steps,
#         "tra_dist": tra_dist,
#         "log_act_dist": log_act_dist,
#         "very_act_dist": very_act_dist
#     }

#     return jsonify(trace)




if __name__ == "__main__":
    app.run(debug = True)