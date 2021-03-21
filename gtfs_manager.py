#!/usr/bin/env python3

from logger import *
import json
import csv
import os

def gtfsToJSON(gtfsName):
    i = 0
    array = []
    json = {}
    with open('data/{}.txt'.format(gtfsName), 'r') as file:
        keysLine = file.readline().split(',')
        for line in csv.reader(file):
            for part in line:
                json[str(keysLine[i])] = str(part)
                i += 1
            i = 0
            json_copy = json.copy()
            array.append(json_copy)
    return(array)
    array.clear()
    json.clear()

def searchInDict(gtfsArrayName, key, value, fitting):
    result = []
    for dictPart in gtfsArrayName:
        if fitting == 'in':
            if str(value) in dictPart[str(key)]:
                result.append(dictPart.copy())
        if fitting == 'is':
            if str(value) == dictPart[str(key)]:
                result.append(dictPart.copy())
    return(result)
    result.clear()

def downloadFiles():
    os.system('wget -O data/gtfs_data.zip http://szegedimenetrend.hu/google_transit.zip &> /dev/null')
    os.system('unzip data/gtfs_data.zip -d data/ &> /dev/null')
    os.system("md5 data/gtfs_data.zip | awk '{ print $4 }' >data/gtfsHash")
    os.system('rm data/gtfs_data.zip')

def updateData():
    if not os.path.exists('data'):
        os.system('mkdir data')
    if not os.path.exists('data/gtfsHash'):
        downloadFiles()
    else:
        os.system('wget -O data/gtfs_tmp.zip http://szegedimenetrend.hu/google_transit.zip &> /dev/null')
        newFileHash = os.system("md5 data/gtfs_tmp.zip | awk '{ print $4 }'")
        oldFileHash = os.system('cat data/gtfsHash')
        if newFileHash != oldFileHash:
            os.system('rm -rf data/*')
            downloadFiles()
