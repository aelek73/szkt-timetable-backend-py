#!/usr/bin/env python3

import json
import csv

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

def searchInDict(gtfsArrayName, key, value):
    result = None
    for dictPart in gtfsArrayName:
        if dictPart[str(key)] == str(value):
            result = dictPart
            break
    return(result)
