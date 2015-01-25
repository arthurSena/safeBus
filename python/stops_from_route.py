# -*- coding: utf-8 -*-
#Falta tratar o caso de ter uma parada próxima apenas à última marcação. Se for o caso é só mudar no for uma coisa.
#Esta abordagem admite que a rota não passa pela mesma parada mais de uma vez no mesmo trajeto. Creio que isso não
#aconteça. Se acontecer amanhã falo outra solução mais elaborada que pensei

from geographiclib.geodesic import Geodesic
import  GEOUtils, IOUtils, routes_manager, KML_manager
import cProfile, math
import csv

#retorna uma lista das paradas de uma rota
import paths


def find_stops_routes(crimes,route_marks):
    stops_route = []
    '''dicionário que terá o valor da distância da parada para a marcação da rota mais próxima'''
#    distance_stops_to_route = {}
    crimes_already_addded = {}
    for i in range(0,len(route_marks)):
        current_mark = route_marks[i]
        near_crimes = get_stops_nearby(current_mark,crimes)

#         '''vai iterar nas paradas próximas a marcação. Se ela não tiver sido adicionada anteriormente nas paradas da rota, adiciona ela
#         tanto na lista das rotas quanto no dicionário contendo a distância da parada à marcação. Se ela já tiver sido adicionado anteriormente
#         verifica se a distância à marca atual é menor que a última distância cadastrada. Se for atualiza e coloca esta parada na nova posição'''
        for crime in near_crimes:
            if not (crime['RUA'] in crimes_already_addded.keys()):
                crimes_already_addded[crime['RUA']] = crime
#             '''Se parada já tiver sido adicionada'''
# #            if (stop[0]["stop_id"] in distance_stops_to_route.keys()):
#             '''se a distância atual da parada à rota for menor que a distância anteriomente cadastrada'''
#             if (stop[1] < distance_stops_to_route[stop[0]["stop_id"]]):
#                 stops_route.remove(stop[0])
# #                else:
# #                    continue
#             stops_route.append(stop[0])
#             distance_stops_to_route[stop[0]["stop_id"]] = stop[1]
    return crimes_already_addded

# recebe uma lista de paradas possiveis e retorna lista de paradas proximas a uma distancia limite do ponto1 
def get_stops_nearby(current_mark,crimes):
    lat1,lon1 = float(current_mark["shape_pt_lat"]),float(current_mark["shape_pt_lon"])
    #limite em metros de distância
    LIMIT = 15
    crimes_proximos = []
    for crime in crimes:
        lat3,lon3 = float(crime["lat"]),float(crime["lon"])
        #verifica distância maxima e direção da parada
        distance = GEOUtils.distance2(lat1,lon1,lat3,lon3)
        print distance

        if (distance <= LIMIT):
            crimes_proximos.append(crime)
    return crimes_proximos

def execute():
    with open("dados/rotas.csv", 'rb') as csvfile:

        listaRotas = csv.reader(csvfile)
        for rota in listaRotas:

            crimes = IOUtils.read_file_to_dictlist('crimes_list.csv')
            #route_marks = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + "shapes.txt")
            route_marks = KML_manager.extract_routes("dados/Rotas.kml")
            marks = IOUtils.lists_to_dicts(route_marks)

            marks2 = routes_manager.marks_from_route(marks,"500")
            paradas = find_stops_routes(crimes,marks2)
            a = 1

cProfile.run('execute()')