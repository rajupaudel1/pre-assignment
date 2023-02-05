from flask import Flask, jsonify

from backend.backend import Backend

backend = Backend()
app = Flask(__name__)


@app.route('/journeylist')
def journey_list():
    data = backend.list_journey()

    # pandas function can generate html table
    return data.to_html(header="true", table_id="table")

app.run()