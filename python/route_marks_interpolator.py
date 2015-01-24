#!/usr/bin/env python
# -*- coding: utf-8 -*-

import IOUtils, paths ,routes_manager, GEOUtils
from geographiclib.geodesic import Geodesic
import os

#iterar nas coordenadas e adicionar coordenadas entre pontos
#retorna lista com todas as coordenadas ja existentes e seus pontos intermediarios
def put_intermediate_points_on_route(max_distance, list_coords):
    list_coords_aux = []
    for i in range(len(list_coords) - 1):
        lat1 = float(list_coords[i]["shape_pt_lat"])
        lon1= float(list_coords[i]["shape_pt_lon"])
        lat2 = float(list_coords[i+1]["shape_pt_lat"])
        lon2 = float(list_coords[i+1]["shape_pt_lon"])
        #adiciona primeiro elemento que está sendo comparado
        list_coords_aux.append((lat1,lon1))
        if GEOUtils.distance2(lat1,lon1,lat2,lon2) > max_distance:
            #adiciona pontos intermediarios
            list_coords_aux.extend(put_intermediate_points(lat1,lon1,lat2,lon2, max_distance))
        #adiciona ultimo elemento da lista original
        if (i == len(list_coords) - 2):
            list_coords_aux.append((list_coords[i + 1]["shape_pt_lat"],list_coords[i+ 1]["shape_pt_lon"]))

    return list_coords_aux

#retorna a quantidade de pontos entre dois pontos dados com uma distância maxima
def calculate_number_of_points(lat1, lon1, lat2, lon2, max_distance):
    distance_between_two_points = GEOUtils.distance2(lat1,lon1,lat2,lon2)

    if distance_between_two_points == 0:
        return 0

    #distancia total entre os dois pontos
    if distance_between_two_points % max_distance == 0:
        return distance_between_two_points/max_distance - 1
    else:
        return int(distance_between_two_points/max_distance)

#retorna lista de pontos intermediários entre dois pontos dados com uma distância maxima
def put_intermediate_points(lat1, lon1, lat2, lon2, max_distance):
    list_points_itermediates = []

    #calcula a quantidade de pontos
    number_of_points = calculate_number_of_points(lat1, lon1, lat2, lon2, max_distance)

    coord = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)

    #distancia entre os pontos intermediarios de dois pontos principais
    distance_between_points = coord['s12'] / (number_of_points + 1)

    #adiciona na lista os pontos intermediarios
    for i in range(number_of_points):
        coord_actual = Geodesic.WGS84.Direct(coord["lat1"], coord["lon1"], coord['azi1'], (i+1)*distance_between_points)
        list_points_itermediates.append((coord_actual["lat2"], coord_actual["lon2"]))

    return list_points_itermediates

# retorna as marcações no formato do transit
def format_transit_points(max_distance, list_coords):
    list_id = []
    answer = [("shape_id","shape_pt_lat","shape_pt_lon","shape_pt_sequence")]
    for element in list_coords:
        list_id.append(element["shape_id"])
    list_id = IOUtils.unique_element(list_id)
    for element in list_id:
        sequence = 1
        list_marks = put_intermediate_points_on_route(max_distance, routes_manager.marks_from_route(list_coords,element))
        for el in list_marks:
            list_aux = []
            answer.append((element,str(el[0]),str(el[1]),str(sequence)))
            sequence += 1
    return answer

# #escreve novos pontos em novo arquivo
# def write_new_points_on_file(route, list_file):
#     list_coords = put_intermediate_points_on_route(route,10, list_file)
#     resp = ""
#
#     for i in range(len(list_coords)):
#         resp += str(route) + "," + str(list_coords[i][0])+ "," + str(list_coords[i][1]) + "," + str(i + 1) + "\n"
#
#     #os.chdir("../../dados/googleTransit/shapesRotas")
#     file_save = open(paths.ROTAS + "novasRotas/" +str(route)+".txt", "w")
#     file_save.write(resp)
#     file_save.close()


# if __name__ == '__main__':
#     # write_new_points_on_file("500", IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT+"shapes.txt"))
#     routes_marks = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT+"/shapesRotas/shapes.txt")
#     marks_500 = routes_manager.marks_from_route(routes_marks,550)
#     print (put_intermediate_points_on_route(10,routes_marks))
