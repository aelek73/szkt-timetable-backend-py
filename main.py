import os
from gtfs_manager import *
import flask
from flask_cors import CORS
from flask import request, jsonify

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def server_running():
    return jsonify('Server is running')

@app.route('/api/v1/agency', methods=['GET'])
def show_agencies():
    return jsonify(gtfsToJSON('agency'))

@app.route('/api/v1/routes/agency_id/<agency_id>', methods=['GET'])
def show_routes_by_agency_id(agency_id):
    return jsonify(searchInDict(gtfsToJSON('routes'), 'agency_id', str(agency_id), 'is'))

@app.route('/api/v1/<dataArray>/<path:pars>', methods=['GET'])
def agencySearch(dataArray, pars):
    if len(pars.split('/')) >= 3:
        key = pars.split('/')[0]
        value = str(pars.split('/')[1]) + '/' + str(pars.split('/')[2])
    else:
        key = pars.split('/')[0]
        value = pars.split('/')[1]
    return jsonify(searchInDict(gtfsToJSON(dataArray), key, value, 'in'))

if __name__ == '__main__':
    updateData()
    app.run()
