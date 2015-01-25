# -*- coding: utf-8 -*-

__author__ = 'andryw'
import csv
import GEOUtils, IOUtils, routes_manager, KML_manager

def execute():
    with open("dados/rotas.csv", 'rb') as csvfile:

        listaRotas = csv.reader(csvfile)
        for rota in listaRotas:
            rota = rota[0]
            route_marks = KML_manager.extract_routes("dados/Rotas.kml")
            marks = IOUtils.lists_to_dicts(route_marks)
            distance = 0
            marks2 = routes_manager.marks_from_route(marks,rota)
            for index in range(0,len(marks2) - 1):
                firstMark = marks2[index]
                secondMark = marks2[index+1]
                distance += GEOUtils.distance2(firstMark['shape_pt_lat'],firstMark['shape_pt_lon'],secondMark['shape_pt_lat'],secondMark['shape_pt_lon'])
            #paradas = find_stops_routes(crimes,marks2)
            a = 1
execute()