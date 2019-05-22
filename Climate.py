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

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"Precipitation Analysis:   /api/v1.0/precipitation<br/>"
        f"Stations:   /api/v1.0/stations<br/>"
        f"Temps:   /api/v1.0/tobs<br/>"
        f"Start:   /api/v1.0/<start><br/>"
        f"Start and End:  /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        prcp = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date > one_year).\
                order_by(Measurement.date).all()
        precipitation = dict(prcp)
        return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
        stat = session.query(Station.station)
        stations = list(stat)
        return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
        one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        temp = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date > one_year).\
                order_by(Measurement.date).all()
        temperature = dict(temp)
        return jsonify(temperature)

## def daily_normals(date):
  ##  sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
 ##   return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()   
##daily_normals("01-01")

@app.route("/api/v1.0/<start>")
def start(start):
        start1 = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        starting = list(start1)
        return jsonify(starting)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
        start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        Ending = list(start_end)
        return jsonify(Ending)

if __name__ == "__main__":
    app.run(debug=True)        