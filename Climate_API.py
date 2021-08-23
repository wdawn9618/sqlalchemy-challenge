from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measure = Base.classes.measurement
Stat = Base.classes.station
session = Session(engine)
route = Flask(_name_)
#Home Page
@app.route("/")
def home():
    """List All Available API Routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-06-20<br/>"
        f"/api/v1.0/2017-06-20/2017-06-28"
    )

#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        prior_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        precip_data = session.query(Measure.date, Measure.prcp).\
            filter(Measure.date >= prior_year).orderby(Measure.date).all()
        precip_dict = dict(precip_data)
        return jsonify(precip_dict)
    

 #Station Route
@app.route("/api/v1.0/stations")
def stations():
    stat_list = session.query(Stat.station, Stat.name).all()
    stations_list = list(stat_list)
    return jsonify(stations_list)

#TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():
        prior_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs = session.query(Measure.date, Measure.tobs).\
                filter(Measure.date >= prior_year).\
                order_by(Measure.date).all()
        tobs_list = list(tobs)
        
        return jsonify(tobs_list)

#Start Routes
@app.route("/api/v1.0/<start>/<end>")
def end_route(start, end):
        end_route = session.query(Measure.date, func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
                filter(Measure.date >= start).\
                filter(Measure.date <= end).\
                group_by(Measure.date).all()
        end_list = list(end_route)
        return jsonify(end_list)

if __name__ == '__main__':
    app.run(debug=True)   