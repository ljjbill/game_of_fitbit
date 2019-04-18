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


# creates a route for the flask front end
@app.route('/')
def home():
   """Return the homepage"""
   return render_template('index.html')

@app.route('/form')
def open_form():
   """go to form page"""
   return render_template('form.html')

class Vital(db.Model):
    __tablename__ = 'vital'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    test = db.Column(db.Integer)

    def __repr__(self):
        return '<Vital %r>' % (self.name)


@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    db.drop_all()
    db.create_all()
    if request.method == "POST":
        age = request.form["userAge"]
        height = request.form["userHeight"]
        weight = request.form["userWeight"]
        test = request.form["userDistance"]
        vital = Vital(age=age, height=height, weight=weight, test=test)
        db.session.add(vital)
        db.session.commit()
        return redirect("/api/vitals", code=302)

    return render_template("form.html")


# create route that returns data for plotting
@app.route("/api/vitals")
def pals():
   

    results = db.session.query(Vital.age,Vital.height,Vital.weight, Vital.test).first()

    age = results[0]
    height = results[1]
    weight = results[2]
    test = results[3]

    trace = {
        "age": age,
        "height": height,
        "weight": weight,
        "test": test
    }

    return jsonify(trace)


""" EXAMPLE
@app.route('/api/pie_chart', methods=['GET'])
def get_medals_percent():
   #Returns Country list with medals percent of all time
   athlete_events = Base.classes.athlete_events
   noc_regions = Base.classes.noc

   sel = [
    noc_regions.region,
    athlete_events.Medal
   ]

   query = db.session.query(*sel)\
         .filter(athlete_events.NOC == noc_regions.NOC)\
         .filter(athlete_events.Season == 'Summer')\
         .filter(athlete_events.Medal.isnot(None))\
         .all()

   df = pd.DataFrame(query)

   df = df.groupby(['region'])

   table = df["Medal"].count().reset_index()
   Total = table['Medal'].sum()

   table['measure'] = round((table['Medal'] / Total), 10)

   name_dict = {
      'region': 'country'
   }

   column_list = [
      'country',
      'measure'
   ]

   table = table.rename(columns=name_dict)
   table = table[table.columns.intersection(column_list)]

   table = table.sort_values(by=['measure'], ascending=False)

   data = table.to_json(orient='records')
   return data
"""

if __name__ == "__main__":
    app.run(debug = True)