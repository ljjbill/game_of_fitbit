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

"""
# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///database/db.sqlite"
db = SQLAlchemy(app)

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