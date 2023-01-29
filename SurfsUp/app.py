# Import Dependencies
import numpy as np
import pandas as pd 
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from   sqlalchemy.ext.automap import automap_base
from   sqlalchemy.orm import Session
from   sqlalchemy import create_engine, func

# Special Dependency for flask
from   flask import Flask, jsonify

# Dependencies for date data
from datetime import datetime, timedelta
from dateutil.relativedelta import *

#################################################
# Database Setup
#################################################
database_path = "../Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save a reference to those classes called `Station` and `Measurement`
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
# Create API welcome page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my HAWAII CLIMATE API<br/>"
        f"<br/>"
        f"Available Options:<br/>"
        f"<br/>"
        f"Precipitation Data: 		/api/v1.0/precipitation<br/>"
    	f"Station List:       		/api/v1.0/stations<br/>"
		f"Temperatire Observations: /api/v1.0/tobs<br/>"
		f"<br/>"
		F"For the following, replace start or end with dates in this format: yyy-mm-dd<br/>"
		f"Starting date only:  /api/v1.0/start<br/>"
		f"Range of dates:      /api/v1.0/start/end "
	)

# Flask route for precipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():

	# Create our session (link) from Python to the DB
	session = Session(engine)

	#Calculate the date 1 year ago from last date in database
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	# Design a query to retrieve the last 12 months of precipitation data.
	precipitation = session.query(Measurement.date, Measurement.prcp).\
		filter(Measurement.date >= prev_year).all()
	
	session.close()

	# Convert the query results to a Dictionary using `date` as the key and `tobs` as the value
	precip = {date: prcp for date, prcp in precipitation}
	# Return the json representation of your dictionary
	return jsonify(precip)

# Flask route for stations analysis
@app.route("/api/v1.0/stations")
def stations():
	# Create our session (link) from Python to the DB
	session = Session(engine)
	
	# Design a query to retrieve a JSON list of stations from the dataset.
	result = session.query(Station.station).all()
	
	session.close()

	# Convert the query results to a list 
	stations = list(np.ravel(result))

	# Return the json representation of your dictionary
	return jsonify(stations)

# Route for temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs(): 
	# Create our session (link) from Python to the DB
	session = Session(engine)
	
	# Design a query to find the most active station
	most_active_station = session.query(Measurement.station).\
    	group_by(Measurement.station).\
    	order_by(func.count(Measurement.date).\
    	desc()).first()

	# Storing first column value as the most active station
	most_active_station_id = most_active_station[0]
	print(f"The most active station is: ",most_active_station_id)

	# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
	most_active = session.query(Measurement.date).\
    	order_by(Measurement.date.desc()).\
		filter(Measurement.station == most_active_station_id).first()

	# Store first column value to identify the latest observation date
	latest_date = most_active[0]

	# Format the date as YYY-MM-DD
	latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
	latest_date = latest_date.date()

	# Calculate the date for exactly one year from the latest observation date
	date_year_ago = latest_date - relativedelta(years=1)

	# Filter the data from the last year date
	last_year_data = session.query(Measurement.date, Measurement.tobs).\
		filter(Measurement.station == most_active_station_id).\
		filter(Measurement.date >= date_year_ago).all()

	# Create a df with only the date and total observations per date
	last_year_data = pd.DataFrame(last_year_data, columns=['date', 'total_obs'])
	
	values = last_year_data.values.tolist()

	session.close()

	# Return the json representation of your dictionary
	return jsonify(values)


# Routes for starting date and range of dates
@app.route("/api/v1.0/<start_date>", defaults={'end_date':None})
@app.route("/api/v1.0/<start_date>/<end_date>")
def datefilter(start_date, end_date):

	# check date format
    try:
        dt.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return 'Enter start date in yyyy-mm-dd format.'

    datedict = {'from':start_date,
                'to':end_date}

    # Create our session (link) from Python to the DB
    session = Session(engine)    

    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    if not end_date:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).all()
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.  
    else:
	       results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        
    calc_temps = pd.DataFrame(results, columns=['TMIN','TAVG','TMAX']).to_dict()

    session.close()

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify([datedict, calc_temps])

# Define main behavior to run de app
if __name__ == ("__main__"):
	app.run(debug=True)
