#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import IOUtils, GEOUtils, paths, routes_manager
from geographiclib.geodesic import Geodesic

# shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence



# Calcula as distancia entre dois pontos a partir de uma colecao de pontos dada
# Recebe o primeiro ponto(first_stop) e o ultimo (last_stop), o ID da rota que quer calcular(route_id),
# a lista (de dicionarios)de todas as rotas(routes_marks), e a lista (de dicionario) de todas as paradas (list_stops)

def stops_distance(first_stop, last_stop, routes_marks,list_stops):

    result = []

    first_stop_coords = stop_coordinates(first_stop["stop_id"],list_stops)
    last_stop_coords = stop_coordinates(last_stop["stop_id"],list_stops)

    index_start = closest_mark_from_stop(first_stop_coords, routes_marks)
    index_finish = closest_mark_from_stop(last_stop_coords, routes_marks)

    if index_start<= index_finish:
        for i in range(index_start, index_finish):
            result.append(
                GEOUtils.distance2(float(routes_marks[i]["shape_pt_lat"]), float(routes_marks[i]["shape_pt_lon"]),
                        float(routes_marks[i+1]["shape_pt_lat"]), float(routes_marks[i+1]["shape_pt_lon"])))
    else:
        for i in range(index_start, len(routes_marks)-1):
            result.append(
                GEOUtils.distance2(float(routes_marks[i]["shape_pt_lat"]), float(routes_marks[i]["shape_pt_lon"]),
                        float(routes_marks[i+1]["shape_pt_lat"]), float(routes_marks[i+1]["shape_pt_lon"])))
        for i in range(0, index_finish):
            result.append(
                GEOUtils.distance2(float(routes_marks[i]["shape_pt_lat"]), float(routes_marks[i]["shape_pt_lon"]),
                        float(routes_marks[i+1]["shape_pt_lat"]), float(routes_marks[i+1]["shape_pt_lon"])))

    return sum(result)


# Retorna corrdenadas de uma parada, buscando pelo ID dela em uma lista de paradas
def stop_coordinates(stopid,stops_list):
    if stops_list is not None:
        for stop in stops_list:
            if stop["stop_id"] == stopid:
                return {"lat":float(stop["stop_lat"]),"lon":float(stop["stop_lon"])}
    return None



# Recebe stopcoords(coordenadas -lat e lon- de uma parada em formato de dicionario) e route_marks (pontos da rota)
#  Retorna o indice na lista route_marks da marcação mais próxima da parada
def closest_mark_from_stop(stopcoords, route_marks):
    if ((stopcoords is None) or len(stopcoords)==0 or (route_marks is None) or len(route_marks)==0):
        return None
    else:
        minimum_distance_start = sys.float_info.max
        right_start = 0
        for i in range(0, len(route_marks)):
            lat_mark = float(route_marks[i]["shape_pt_lat"])
            lon_mark = float(route_marks[i]["shape_pt_lon"])
            distance = GEOUtils.distance(float(stopcoords["lat"]), float(stopcoords["lon"]), lat_mark,lon_mark)

            if distance < minimum_distance_start:
                minimum_distance_start = distance
    #            right_start = route_marks[i]["shape_pt_sequence"]
                right_start = i
        return right_start

# Retorna uma lista de pontos ~ possivelmente ~ repetidos entre o conjunto de pontos passados
# def repeated_points():
# 	stops_list = IOUtils.stops_file()
# 	repeated_stops = ["stop_id,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url"]
	
# 	for i in range(1, len(stops_list)-2):
# 		lis = str(stops_list[i]).split(",")
# 		name = lis[0]
# 		lat = lis[3]
# 		lon = lis[4]

# 		lis_pos = str(stops_list[i+1]).split(",")
# 		name_pos = lis_pos[0]
# 		lat_pos = lis_pos[3]
# 		lon_pos = lis_pos[4]
# 		distance = GEOUtils.distance(float(lat), float(lon), float(lat_pos), float(lon_pos))

# 		if distance <= 40.0:
# 		    repeated_stops.append(str(stops_list[i]))
            
	#IOUtils.save_file(repeated_stops, "teste.txt")
	# return repeated_stops

# Retorna uma lista de pontos ~ possivelmente ~ repetidos entre o conjunto de pontos passados
def repeated_points(all_stops):
    repeated_stops = []
    for i in range(0, len(all_stops)-1):
        for j in range(i+1, len(all_stops)):
            distance = GEOUtils.distance2(float(all_stops[i]["stop_lat"]), float(all_stops[i]["stop_lon"]), float(all_stops[j]["stop_lat"]), float(all_stops[j]["stop_lon"]))
            if distance <= 5.0:
                repeated_stops.append((all_stops[i], all_stops[j]))
    return repeated_stops

# if __name__ == '__main__':
#     print repeated_points(IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT+"stops.txt"))
