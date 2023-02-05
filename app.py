from flask import Flask

from backend.backend import Backend

backend = Backend()
app = Flask(__name__)


@app.route('/journeylists')
def journey_list():
    data = backend.list_journey()

    # pandas function can generate html table
    return data.to_html(header="true", table_id="table")


@app.route('/stations')
def station_list():
    station_data = backend.load_meta_data()

    # in case if there are multiple stations id found, then displaying only one is enough as this is same information
    station_data = station_data.groupby('ID').first()

    # pandas function can generate html table
    return station_data.to_html(header="true", table_id="table")


@app.route('/station_infos')
def station_info():
    station_return_departure = backend.departure_return_info()
    return station_return_departure.to_html(header="true", table_id="table")


app.run()
