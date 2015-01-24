# -*- coding: utf-8 -*-
#Falta tratar o caso de ter uma parada próxima apenas à última marcação. Se for o caso é só mudar no for uma coisa.
#Esta abordagem admite que a rota não passa pela mesma parada mais de uma vez no mesmo trajeto. Creio que isso não
#aconteça. Se acontecer amanhã falo outra solução mais elaborada que pensei

from geographiclib.geodesic import Geodesic
import  GEOUtils, IOUtils, routes_manager, KML_manager
import cProfile, math

#retorna uma lista das paradas de uma rota
import paths


def find_stops_routes(stops,route_marks):
    possible_stop = stops
    stops_route = []
    '''dicionário que terá o valor da distância da parada para a marcação da rota mais próxima'''
    distance_stops_to_route = {}

    for i in range(0,len(route_marks)):
        current_mark = route_marks[i]
        '''pega paradas próximas a marcação atual'''
        near_stops = get_stops_nearby(current_mark,possible_stop)

        '''vai iterar nas paradas próximas a marcação. Se ela não tiver sido adicionada anteriormente nas paradas da rota, adiciona ela
        tanto na lista das rotas quanto no dicionário contendo a distância da parada à marcação. Se ela já tiver sido adicionado anteriormente
        verifica se a distância à marca atual é menor que a última distância cadastrada. Se for atualiza e coloca esta parada na nova posição'''
        for stop in near_stops:
            '''Se parada já tiver sido adicionada'''
            if (stop[0]["stop_id"] in distance_stops_to_route.keys()):
                '''se a distância atual da parada à rota for menor que a distância anteriomente cadastrada'''
                if (stop[1] < distance_stops_to_route[stop[0]["stop_id"]]):
                    stops_route.remove(stop[0])
                else:
                    continue
            stops_route.append(stop[0])
            distance_stops_to_route[stop[0]["stop_id"]] = stop[1]
    return stops_route

# recebe uma lista de paradas possiveis e retorna lista de paradas proximas a uma distancia limite do ponto1 
def get_stops_nearby(current_mark,possible_stop):
    lat1,lon1 = float(current_mark["shape_pt_lat"]),float(current_mark["shape_pt_lon"])
    #limite em metros de distância
    LIMIT = 15
    stops_nearby = []
    for stop in possible_stop:
        lat3,lon3 = float(stop["stop_lat"]),float(stop["stop_lon"])
        #verifica distância maxima e direção da parada
        distance = GEOUtils.distance2(lat1,lon1,lat3,lon3)
        if (distance <= LIMIT):
            stops_nearby.append([stop,distance])
    return sorted(stops_nearby, key=lambda tup: tup[1])

def execute():
     stops = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + 'stops.txt')
     #route_marks = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + "shapes.txt")
     route_marks = KML_manager.extract_routes(paths.ROTAS + "Rotas.kml")
     marks = IOUtils.lists_to_dicts(route_marks)

     marks2 = routes_manager.marks_from_route(marks,"904")
     paradas = find_stops_routes(stops,marks2)
     KML_manager.write_stops(paradas,"teste1.kml")
#     a = 1
# #print(paradasOi)
# #thefile = open('paradas_500.txt', 'w')netshoes@info.netshoes.com.br
# #for item in paradasOi:
# #    thefile.write("%s\n" % item)#
#
# def teste():
#     route_marks = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + "shapes.txt")
#     route_marks = route_marks[:100]
#     lista1 = []
#     for j in range(len(route_marks)):
#         for i in range(len(route_marks)):
#             a = GEOUtils.distance(route_marks[i]["shape_pt_lat"],route_marks[i]["shape_pt_lon"],route_marks[i]["shape_pt_lat"],route_marks[i]["shape_pt_lon"])
#             b = GEOUtils.distance2(route_marks[i]["shape_pt_lat"],route_marks[i]["shape_pt_lon"],route_marks[i]["shape_pt_lat"],route_marks[i]["shape_pt_lon"])
#             lista1.append((a-b))
#     print reduce(lambda x, y: x + y, lista1) / len(lista1)
#     a = 1
#cProfile.run('execute()')