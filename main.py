from gtfs_manager import *
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify('Server is running')

@app.route('/api/v1/<dataArray>', methods=['GET'])
def api_all(dataArray):
    return jsonify(gtfsToJSON(dataArray))

@app.route('/api/v1/<dataArray>/<key>/<value>', methods=['GET'])
def agencySearch(dataArray, key, value):
    return jsonify(searchInDict(gtfsToJSON(dataArray), key, value))

app.run()
