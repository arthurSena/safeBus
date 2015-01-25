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

        for crime in near_crimes:
            if not (crime['RUA'] in crimes_already_addded.keys()):
                crimes_already_addded[crime['RUA']] = crime

    return crimes_already_addded

# recebe uma lista de paradas possiveis e retorna lista de paradas proximas a uma distancia limite do ponto1 
def get_stops_nearby(current_mark,crimes):
    lat1,lon1 = float(current_mark["shape_pt_lat"]),float(current_mark["shape_pt_lon"])
    #limite em metros de distância
    LIMIT = 200
    crimes_proximos = []
    for crime in crimes:
        lat3,lon3 = float(crime["lat"]),float(crime["lon"])
        #verifica distância maxima e direção da parada
        distance = GEOUtils.distance2(lat1,lon1,lat3,lon3)
        #print distance

        if (distance <= LIMIT):
            crimes_proximos.append(crime)
    return crimes_proximos

def execute():
    with open("dados/rotas.csv", 'rb') as csvfile:

        listaRotas = csv.reader(csvfile)
        for rota in listaRotas:

            crimes = IOUtils.read_file_to_dictlist('crimes_list3.csv')
            #route_marks = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + "shapes.txt")
            route_marks = KML_manager.extract_routes("dados/Rotas.kml")
            marks = IOUtils.lists_to_dicts(route_marks)

            marks2 = routes_manager.marks_from_route(marks,rota[0])
            paradas = find_stops_routes(crimes,marks2)
            total_crimes = 0
            for parada in paradas:
                total_crimes += int(paradas[parada]["count"])
            print str(rota[0])+","+str(total_crimes)
            a = 1

cProfile.run('execute()')