from flask import Flask, jsonify

from backend.backend import Backend

backend = Backend()
app = Flask(__name__)


@app.route('/journeylist')
def journey_list():
    data = backend.list_journey()

    # pandas function can generate html table
    return data.to_html(header="true", table_id="table")


@app.route('/station')
def station_list():
    station_data = backend.load_meta_data()

    # in case if there are multiple stations id found, then displaying only one is enough as this is same information
    station_data = station_data.groupby('ID').first()

    # pandas function can generate html table
    return station_data.to_html(header="true", table_id="table")

@app.route('/station_info')
def station_info():
    station_info = backend.depature_return_info()
    return station_info.to_html(header="true", table_id="table")

app.run()

