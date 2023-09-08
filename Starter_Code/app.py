# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import re

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///C:\\Users\\noahs\\Desktop\\Class Assignments\\Module_10_Challenge\\Starter_Code\\Resources\\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

#1 HOME
@app.route("/")
def welcome():
    return (
        f"Hawaii Climate Analysis<br/>"
        
        f"Routes:<br/>"
        
        f"/api/v1.0/precipitation<br/>"
        
        f"/api/v1.0/stations<br/>"
        
        f"/api/v1.0/tobs<br/>"
        
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )



#2 PRECIPITATION
@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)

    one_year= dt.date(2017, 8, 23)-dt.timedelta(days=365)
    
    prev_last_date = dt.date(one_year.year, one_year.month, one_year.day)

    results= session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= prev_last_date).\
            order_by(measurement.date.desc()).all()


    p_dict = dict(results)

    print(f"Precipitation Results : {p_dict}")
    
    return jsonify(p_dict)



#3 STATIONS
@app.route("/api/v1.0/stations")

def stations():
    
    session = Session(engine)
    
    sel = [station.station, station.name, station.latitude, station.longitude, station.elevation]
    
    query = session.query(*sel).all()
    
    session.close()

    stations = []
    
    for station,name,lat,lon,ele in query:
    
        station_dict = {}
    
        station_dict["Station"] = station
    
        station_dict["Name"] = name
    
        station_dict["Lat"] = lat
    
        station_dict["Lon"] = lon
    
        station_dict["Elevation"] = ele
    
        stations.append(station_dict)

    return jsonify(stations)


#4 TOBS
@app.route("/api/v1.0/tobs")

def tobs():
     
     session = Session(engine)


     query = session.query( measurement.date, measurement.tobs).\
        filter(measurement.station=='USC00519281')\
     .filter(measurement.date>='2016-08-23').all()


     tob_obs = []
     
     for date, tobs in query:
        
         tobs_dict = {}
        
         tobs_dict["Date"] = date
         
         tobs_dict["Tobs"] = tobs
         
         tob_obs.append(tobs_dict)

     return jsonify(tob_obs)


#5 START
@app.route("/api/v1.0/<start>")

def start(start):
    
    session = Session(engine)
    
    query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date >= start).all()
    
    session.close()

    temps = []
    
    for min_temp, avg_temp, max_temp in query:
    
        temps_dict = {}
    
        temps_dict['Minimum Temperature'] = min_temp
    
        temps_dict['Average Temperature'] = avg_temp
    
        temps_dict['Maximum Temperature'] = max_temp
    
        temps.append(temps_dict)

    return jsonify(temps)


#5 START TO END
@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    
    session = Session(engine)
    
    query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()

    
    temps = []
    
    for min_temp, avg_temp, max_temp in query:
    
        temps_dict = {}
    
        temps_dict['Minimum Temperature'] = min_temp
    
        temps_dict['Average Temperature'] = avg_temp
    
        temps_dict['Maximum Temperature'] = max_temp
    
        temps.append(temps_dict)

    return jsonify(temps)




if __name__ == '__main__':
    
    app.run(debug=True)