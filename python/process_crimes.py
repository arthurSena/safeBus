# -*- coding: utf-8 -*-

__author__ = 'andryw'

import csv
import IOUtils

def crimes_incidence(file_name):
    crimes_street = {}
    with open(file_name, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if not (crimes_street.has_key(row[0])):
                dict_ = dict(lat=row[1], lon=row[2], count=0)
                crimes_street[row[0]] = dict_

            crimes_street[row[0]]["count"] += 1

        # list_maps = IOUtils.lists_to_dicts(archive)

    return crimes_street


def toList(dict_):
    stops = []
    for value in dict_:
        cell = dict_[value]
        stops.append(str(cell["lat"]) + ","+ str(cell["lon"]) + ","+ str(cell["count"]) + "," + str(value))
    return stops


crimes = crimes_incidence("dados/crimes.csv")
crimesList = toList(crimes)
IOUtils.save_file(crimesList,"crimes_list.csv")