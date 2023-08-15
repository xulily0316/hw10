# Import the dependencies.
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import flask
from flask import Flask , jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"welcome page <br/>"
           
        f" routes <br/>"
           
        f"/api/v1.0/precipitation <br/>"
           
        f"/api/v1.0/stations <br/>"
           
        f"/api/v1.0/tobs <br/>"
        )



    
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.prcp, Measurement.date)\
        .filter(Measurement.date > '2016-08-23')\
        .order_by(Measurement.date).all()
    df_results=pd.DataFrame(results)
    df_results=df_results.rename(columns={"prcp":"precipitation"})
    df_results.sort_values(by=['date'], ascending=True, inplace=True)
    df_results.dropna(inplace=True)
    df_results.reset_index(drop=True, inplace=True)
    precip_dict = df_results.to_dict('records')
    return jsonify(precip_dict)    
    

@app.route("/api/v1.0/stations")
def station():
    station_count = session.query(Station.station).all()
    most_active_stations = list(np.ravel(station_count))
    return jsonify(most_active_stations)



@app.route("/api/v1.0/tobs")

def tobs():
    results_temp = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    df_temp = list(np.ravel(results_temp))
    return jsonify (df_temp)


           
@app.route ("/api/v1.0/<start>/<end>")
def temps(start, end):
    findings = session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all()
    
    temps = [temp[0] for temp in findings]
    
    temp_min = min(temps)
    temp_max = max(temps)
    temp_avg = np.mean(temps)
    
    return jsonify({"temp_min": temp_min, "temp_max": temp_max, "temp_avg": temp_avg})

if __name__ == "__main__":
   app.run(debug=True)