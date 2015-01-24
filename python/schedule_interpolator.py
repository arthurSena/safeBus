#!/usr/bin/env python
# -*- coding: utf-8 -*-

import IOUtils, UnityUtils, stops_manager, paths
import time

distances = {}
def is_distance_already_calculated(firstpoint,secondpoint,route):
    return (distances.has_key(route) and distances[route].has_key((firstpoint,secondpoint)))

def distance_already_calculated(firstpoint,secondpoint,route):
    return (distances[route][(firstpoint,secondpoint)])

def distance_calculated(firstpoint,secondpoint,route,distance):
    if (not distances.has_key(route)):
        distances[route]= {}
    distances[route][(firstpoint,secondpoint)] = distance

'''Retorna a tabela de horários das paradas que não tem hora, a partir de uma parada de referência (stop1) e a velocidade (speed)'''
def stops_calculate_schedule_interpolator(stop1, speed, stops, route, list_shapes, stops_info):
    if (len(stops) == 0):
        return []
    initial_time = UnityUtils.change_schedule_second(stop1["departure_time"])
    schedule = []

    '''Calcula o tempo entre a parada de referência passada (stop1) e a primeira parada sem horário'''
    currenttime = initial_time
    currenttime = timetoreachsecondpoint(stop1, stops[0], list_shapes, stops_info,speed,currenttime,route)
    schedule.append([(time.strftime("%H:%M:%S", time.gmtime(currenttime))),stops[0]["stop_id"]])

    '''Calcula o horário para todas as paradas sem horário (excetuando a primeira) '''
    for i in range(1, len(stops)):
        currenttime = timetoreachsecondpoint(stops[i - 1], stops[i], list_shapes, stops_info,speed,currenttime,route)
        schedule.append([(time.strftime("%H:%M:%S", time.gmtime(currenttime))),stops[i]["stop_id"]])

    return schedule

'''Dado a distância, velocidade e tempo inicial calcular o tempo final'''
def calculatetime(distance,speed,initialtime):
    deltatime = distance / float(speed)
    return initialtime + deltatime

'''Dado dois pontos e a velocidade, calcular o tempo final para chegar no segundo ponto'''
def timetoreachsecondpoint(firstpoint,secondpoint,list_shapes,list_stops,speed,initialtime,route):
    if (is_distance_already_calculated(firstpoint['stop_id'],secondpoint['stop_id'],str(route))):
        distance =  distance_already_calculated(firstpoint['stop_id'],secondpoint['stop_id'],str(route))
    else:
        distance = stops_manager.stops_distance(firstpoint, secondpoint, list_shapes, list_stops)
        distance_calculated(firstpoint['stop_id'], secondpoint['stop_id'],str(route),distance)

    return calculatetime(distance,speed,initialtime)

'''Calcula a velocidade para se chegar ao ponto 2 a partir do ponto 1'''
def calculatespeed(stop1,stop2,list_shapes, list_stops):
    schedule_inicial = UnityUtils.change_schedule_second(stop1["departure_time"])
    schedule_final = UnityUtils.change_schedule_second(stop2["departure_time"])
    distance_route_main = stops_manager.stops_distance(stop1, stop2, list_shapes, list_stops)
    speed = distance_route_main / (schedule_final - schedule_inicial)
    if (speed < 0):
        raise ValueError("Negative speed!")
    return speed

'''Interpola o horário das paradas (stops_ids) de uma rota, dada uma lista de paradas que já possuam horário (stop_times)'''
def schedule_interpolator(stops_ids, route, stop_times, route_marks, stops_info_list):
    schedule = []

    '''Cria hash com informações das paradas para auxiliar na performance'''
    stops_info_hash = {stop["stop_id"]:stop for stop in stops_info_list}

    '''Manipula a lista de paradas a serem interpoladas para que a primeira parada da lista seja a primeira parada que possui horário '''
    for stop_time in stop_times:
        stops_list_index = stops_ids.index(stop_time["stop_id"])
        if (stops_list_index > -1):
            stops_ids = stops_ids[stops_list_index:] + stops_ids[:stops_list_index]
            break

    '''Saber quais paradas com horário estão entre as paradas a serem interpoladas (stops_ids) e qual índice.'''
    stops_times_in_stops_list = []
    for stop_time in stop_times:
        stops_list_index = stops_ids.index(stop_time["stop_id"])
        if (stops_list_index > -1):
            stops_times_in_stops_list.append([stops_list_index,stop_time])

    '''Vai interpolar o horário das paradas que estão entre a primeira parada com horário e a última parada com horário'''
    for i in range(0,len(stops_times_in_stops_list)-1):
        first_stop_time = stops_times_in_stops_list[i]
        second_stop_time = stops_times_in_stops_list[i + 1]
        schedule.append([first_stop_time[1]["departure_time"],first_stop_time[1]["stop_id"]])

        '''Paradas que serão interpoladas entre a parada com horário 'i' e a parada com horário 'i+1' '''
        list_stops_to_interpolate = []
        for j in range(first_stop_time[0]+1,second_stop_time[0]):
            list_stops_to_interpolate.append(stops_info_hash[stops_ids[j]])
        speed = calculatespeed(first_stop_time[1],second_stop_time[1],route_marks, stops_info_list)
        schedule.extend(stops_calculate_schedule_interpolator(first_stop_time[1],speed, list_stops_to_interpolate, route, route_marks, stops_info_list))

    '''Calcular o horário das paradas que estão além da última parada com horário'''
    main_speed = calculatespeed(stop_times[0],stop_times[-1],route_marks, stops_info_list)
    last_stop_time = stops_times_in_stops_list[-1]
    schedule.append([last_stop_time[1]["departure_time"],last_stop_time[1]["stop_id"]])
    list_stops_to_interpolate = []
    for j in range(last_stop_time[0]+1,len(stops_ids)):
            list_stops_to_interpolate.append(stops_info_hash[stops_ids[j]])
    if (list_stops_to_interpolate):
        schedule.extend(stops_calculate_schedule_interpolator(last_stop_time[1],main_speed, list_stops_to_interpolate, route, route_marks, stops_info_list))

    return schedule


# if __name__ == '__main__':
#     i = 1
#     list_stop_times = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + "stop_times.txt")
#     list_shapes = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + "shapes.txt")
#     list_stops = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + "stops.txt")
#     # while(True):
#     trip = 'diasUteis_500_' + str(i)
#     stop_times_filtered = [stop_time for stop_time in list_stop_times if stop_time["trip_id"] == trip]
#     resp = schedule_interpolator(
#         ["CANTINHO_UNIVERSITÁRIO_457", "CLINICA_SANTA_MARIA_-_OPOSTO_561", "794_-_OPOSTO_563", "238_-_OPOSTO_564",
#          "310_565",
#          "INTEGRACAO_1", "OI_-_TELEMAR_12",
#          "PRAÇA_CLEMENTINO_PROCÓPIO_140", "PAGUE_FÁCIL_97", "ARCA_CATEDRAL_145", "JUIZADO_DO_CONSUMIDOR_105",
#          "DAMAS_151",
#          "JR_CABELEREIRO_152",
#          "INTEGRACAO_2", "REAL_CLUBE_109", "300_548"], 500, stop_times_filtered, list_shapes, list_stops)
#     print resp
#     i += 1

    # print "----------"
    # i = 1
    # while(True):
    # trip = 'diasUteis_505_'+ str(i)
    # 	if (not IOUtils.stop_time_file().has_key(trip)):
    # 		break
    # 	resp = points_interpolator(["CABRAL_458","UFCG_453","UFCG_451", "LAVA-JATO_-_OPOSTO_454", "CANTINHO_UNIVERSITÁRIO_457", "35_490", "569_-_OPOSTO_492", "425_-_OPOSTO_493", "43_-_LATERAL_494", "EMBRABA_-_OPOSTO_496",
    # 		"INTEGRACAO_1","ARCA_TITÃO_155","OI_-_TELEMAR_12",
    # 		"PRAÇA_CLEMENTINO_PROCÓPIO_140","1044_99", "1054_100", "FEIRA_CENTRAL_13", "BORBÃO_212", "ESCOLA_NORMAL_217",
    # 		"RODOVIÁRIA_430", "POLÍCIA_FEDERAL_221", "40_328", "ABRIGO_JOSE_PINHEIRO_437", "ANTIGO_PHD_146",
    # 		"ALUÍSIO_CALÇADOS_478","10_381", "154_-_OPOSTO_475", "337_483"], trip, 505)
    # 	print resp
    # 	i += 1