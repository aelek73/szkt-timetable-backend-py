from gtfs_manager import *
import flask
from flask_cors import CORS
from flask import request, jsonify

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify('Server is running')

@app.route('/api/v1/<dataArray>', methods=['GET'])
def api_all(dataArray):
    return jsonify(gtfsToJSON(dataArray))

@app.route('/api/v1/<dataArray>/<path:pars>', methods=['GET'])
def agencySearch(dataArray, pars):
    if len(pars.split('/')) >= 3:
        key = pars.split('/')[0]
        value = str(pars.split('/')[1]) + '/' + str(pars.split('/')[2])
    else:
        key = pars.split('/')[0]
        value = pars.split('/')[1]
    return jsonify(searchInDict(gtfsToJSON(dataArray), key, value))

app.run()
