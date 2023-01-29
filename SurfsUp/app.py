
# Import Flask dependencies
from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, extract
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/vosta/OneDrive/Documents/GitHub/sqlalchemy-challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# create a reference of the classes
Station = Base.classes.station

# Save reference to the table
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Using the references to classes, start querying the database
# from sqlalchemy.orm import Session
# from sqlalchemy.orm import scoped_session
# from sqlalchemy.orm import sessionmaker

#Session management with scoped session (Session that is universal across all threads in the code)
#session_factory = sessionmaker(bind=engine)
#Session = scoped_session(session_factory)
#some_session = Session()

# Define what to do when a user hits the index route
#################################################
# Flask Routes 
#################################################
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    """List all available api routes."""
    return (
        f"Hello - Welcome to my climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/preciptation")
def preciptation():
    print("Server received request for 'Precipitation' data...")
        # Create our session (link) from Python to the DB
    session = Session(engine)
    # Querying the database 
    prcp_data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()

    session.close()
    
    # Unpacking the tuple into separate lists
    dates_p = [res[0] for res in prcp_data]
    prcp_p  = [res[1] for res in prcp_data]

    # combining the above lists into dictionary
    prcp_dict = dict(zip(dates_p,prcp_p))
    
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' data...")
    session = Session(engine)
    # querying the db
    stations = session.query(Station.station)
    session.close()
    # unpacking the tuple into separate lists
    station = [res[0] for res in stations]

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations' data...")
    session = Session(engine)
    
    # querying the db
    temp_obs = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <='2017-08-23').all()
    session.close()

    # unpacking the tuple into separate lists
    temp = [res[0] for res in temp_obs]
    
    return jsonify(temp)

@app.route("/api/v1.0/<start_date>")
def temps(start_date):
    return jsonify(Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all())

@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_end(start_date,end_date):
    return jsonify(Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date<= end_date).all())

if __name__ == '__main__':
    app.run(debug=True)
