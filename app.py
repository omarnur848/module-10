# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################
engine =create_engine("sqlite:///Resources/hawaii.sqlite")

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
def date_prev_year():
    # Create the session
    session = Session(engine)

    # Define the most recent date in the Measurement dataset
    # Then use the most recent date to calculate the date one year from the last date
    most_recent_date = session.query(func.max(Measurement.date)).first()[0]
    first_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Close the session                   
    session.close()

    # Return the date
    return(first_date)


@app.route("/")
def homepage():
    return """ <h1> Welcome to Honolulu, Hawaii Climate API! </h1>
    <h3> The available routes are: </h3>
    <ul>
    <li><a href = "/api/v1.0/precipitation"> Precipitation</a>: <strong>/api/v1.0/precipitation</strong> </li>
    <li><a href = "/api/v1.0/stations"> Stations </a>: <strong>/api/v1.0/stations</strong></li>
    <li><a href = "/api/v1.0/tobs"> TOBS </a>: <strong>/api/v1.0/tobs</strong></li>
    <li>To retrieve the minimum, average, and maximum temperatures for a specific start date, use <strong>/api/v1.0/&ltstart&gt</strong> (replace start date in yyyy-mm-dd format)</li>
    <li>To retrieve the minimum, average, and maximum temperatures for a specific start-end range, use <strong>/api/v1.0/&ltstart&gt/&ltend&gt</strong> (replace start and end date in yyyy-mm-dd format)</li>
    </ul>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)


    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_prev_year()).all()
    
    # Close the session                   
    session.close()

    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)


    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)

    # Query station data from the Station dataset
    station_data = session.query(Station.station).all()

    # Close the session                   
    session.close()

# Define main branch 
if __name__ == "__main__":
    app.run(debug = True)