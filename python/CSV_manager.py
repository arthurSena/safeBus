#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paths, IOUtils
import csv

# le o csv das paradas e retorna as retorna no formato do google transit
#stops.txt
def extract_stops(file_name):

	archive = []
	stops = []
	#cabeçalho
	stops.append(["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"])

	with open(file_name, 'rb') as csvfile:
	    spamreader = csv.reader(csvfile, delimiter=',')
	    for row in spamreader:
	    	archive.append(row)

	list_maps = IOUtils.lists_to_dicts(archive)


	for maps in list_maps:
		name = maps["REFERENCIA"].strip().replace(",", "") +"_"+ maps["COD"]
		desc = name.replace(" ", "_")
		stops.append([desc, name, "Rua / Avenida: " + maps["RUA"].replace(",", ""), maps["LATITUDE"], maps["LONGITUDE"],"",""])
	stops.append(["INTEGRACAO_1","INTEGRACAO_1","Rua / Avenida: Dom Pedro II","-7.220618", "-35.889802","",""])
	stops.append(["INTEGRACAO_2","INTEGRACAO_2","Rua / Avenida: Dom Pedro II","-7.220693", "-35.888944","",""])
	return stops
	
# if __name__ == '__main__':
# 	extract_stops("/home/celio/Desenvolvimento/bushour/rotas/dados/paradas/paradas_rotas_original.csv")