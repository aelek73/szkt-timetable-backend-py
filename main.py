import os
from gtfs_manager import *
import flask
from flask_cors import CORS
from flask import request, jsonify

def downloadFiles():
    os.system('wget -O data/gtfs_data.zip http://szegedimenetrend.hu/google_transit.zip &> /dev/null')
    os.system('unzip data/gtfs_data.zip -d data/')
    os.system("md5 data/gtfs_data.zip | awk '{ print $4 }' >data/gtfsHash")
    os.system('rm data/gtfs_data.zip')

def updateData():
    if not os.path.exists('data/gtfsHash'):
        downloadFiles()
    else:
        os.system('wget -O data/gtfs_tmp.zip http://szegedimenetrend.hu/google_transit.zip &> /dev/null')
        newFileHash = os.system("md5 data/gtfs_tmp.zip | awk '{ print $4 }'")
        oldFileHash = os.system('cat data/gtfsHash')
        if newFileHash != oldFileHash:
            os.system('rm -rf data/*')
            downloadFiles()

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

if __name__ == '__main__':
    updateData()
    app.run()
