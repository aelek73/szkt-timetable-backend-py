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

@app.route('/api/v1/trips/route_id/<route_id>', methods=['GET'])
def show_trips_by_route_id(route_id):
    requested_trips = searchInDict(gtfsToJSON('trips'), 'route_id', str(route_id), 'is')

    src = ''
    dst = ''
    for element in requested_trips:
        if src == '':
            src = element['trip_headsign']
        else:
            if src == element['trip_headsign']:
                continue
        if dst == '':
            if src != element['trip_headsign']:
                dst = element['trip_headsign']
            else:
                continue
        if not src == '' and not dst == '':
            break

    for element in requested_trips:
            if not element['trip_headsign'] == src or not element['trip_headsign'] == dst:
                requested_trips.remove(element)
                continue

    for element in requested_trips:
        if element['trip_headsign'] == src:
            element['trip_headsign'] = src + ' -> ' + dst
        if element['trip_headsign'] == dst:
            element['trip_headsign'] = dst + ' -> ' + src

    sorted_trips = sorted(requested_trips, key = lambda x: x['trip_headsign'])
    selected_elements = []
    tmp = ''
    for element in sorted_trips:
        if tmp == '':
            tmp = element['trip_headsign']
            selected_elements.append(element)
        else:
            if element['trip_headsign'] == tmp:
                continue
            else:
                tmp = element['trip_headsign']
                selected_elements.append(element)
                break

    return jsonify(selected_elements)

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
