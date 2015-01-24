#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')
from IOUtils import read_file_to_dictlist
from IOUtils import save_file_lists

def stops_from_especific_route():
    paradas = "../../../dados/googleTransit/stops.txt"
    paradas500 = "../../../dados/paradas/paradas500_manualmente.txt"

    listaparadas = read_file_to_dictlist(paradas)
    listaparadas500 = read_file_to_dictlist(paradas500)

    listafinal500 = []

    precisao = 13

    for p500 in listaparadas500:
        for parada in listaparadas:
            if almost_equal(parada['stop_lat'], p500['stop_lat'], precisao) and almost_equal(parada['stop_lon'], p500['stop_lon'], precisao):
                listafinal500.append(parada)

    return listafinal500

def almost_equal(x, y, decimal_precision):
    return abs(float(x) - float(y)) <= 10**(-1*decimal_precision)

def transform_list_of_dict_to_list_of_lists(list):
    dict_keys = ['stop_id','stop_name','stop_desc','stop_lat','stop_lon','zone_id','stop_url']

    list_of_lists = [dict_keys]

    for i in range(len(list)):
        aux_list = []
        for j in range(len(dict_keys)):
            aux_list.append(list[i].get(dict_keys[j]))
        list_of_lists.insert(i+1,aux_list)

    return list_of_lists


if __name__ == '__main__':
    lista_paradas_500 = stops_from_especific_route()

    answer = transform_list_of_dict_to_list_of_lists(lista_paradas_500)

    save_file_lists(answer, "../../../dados/paradas/paradas500_manualmente_formato_googleTransit.txt")

