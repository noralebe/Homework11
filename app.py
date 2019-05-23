import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>'2016-08-23').all()
    precip = {date:prcp for date, prcp in precipitation }
    return jsonify(precip)

    #"""Convert the query results to a Dictionary using `date` as the key and `prcp` as the value."""
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)
@app.route("/api/v1.0/tobs")    
def tobs():
    tempobs = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date>'2016-08-23').all()
    return jsonify(tempobs)
@app.route("/api/v1.0/start/<start>") 
def start(start):

    tmin=session.query(func.min(Measurement.tobs)).filter(Measurement.date>start).all()   
    tavg=session.query(func.avg(Measurement.tobs)).filter(Measurement.date>start).all()
    tmax=session.query(func.max(Measurement.tobs)).filter(Measurement.date>start).all()
    sel=[tmin, tavg, tmax]
   
    return jsonify(sel) 
       


if __name__ == '__main__':
    app.run(debug=True)
