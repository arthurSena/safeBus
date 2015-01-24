#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')

import IOUtils, paths,routes_manager,stops_from_route,KML_manager

stops = IOUtils.read_file_to_dictlist('../' + paths.GOOGLE_TRANSIT + 'stops.txt')
routes = IOUtils.read_file_to_dictlist('../'+ paths.INTERPOLATED_SHAPES + 'shapes.txt')

stop_ids = []
stop_ids.append("stop_id,route")
for route_name in ["505","500","550","555"]:
    marks = routes_manager.marks_from_route(routes,route_name)
    paradas = stops_from_route.find_stops_routes(stops,marks)

    for i in range(len(paradas)):
        stop_ids.append(paradas[i]["stop_id"] + "," + route_name)

IOUtils.save_file(stop_ids,'../'+paths.PARADAS +"Paradas das rotas.txt")
    #KML_manager.write_stops(paradas,'../' + paths.PARADAS_KML + "paradas" +route_name+".kml","Paradas " +route_name)

