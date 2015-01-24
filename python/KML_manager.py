#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paths, IOUtils
from pykml import parser
from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML

# le o kml das paradas e retorna as retorna no formato do google transit
#stops.txt
def extract_stops(file_name):
    root = parser.fromstring(open(file_name, 'r').read())
    stops = []
    #cabeçalho
    stops.append(["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"])

    for points in root.Document.Folder.Placemark:
        #coordenadas informadas no kml (<Point><coordinates>)
        coord = points.Point.coordinates
        longi,lat,ident = str(coord).split(',')
        longi = longi.replace(" ","")

        htmls = points.description
        htmls = '"'+htmls+'"'
        htmls = htmls.encode('utf8')
        list_htmls = htmls.split("\n")
        reference = ""
        street = ""

        for i in range(0,len(list_htmls)):
            if (list_htmls[i] == '<td>REFERÊNCIA</td>'):
                reference = list_htmls[i+2]
                reference = reference.replace("<td>","")
                reference = reference.replace("</td>","")
                reference = reference.replace(" ","_")
                reference = reference

            if (list_htmls[i] == '<td>RUA</td>'):
                street = list_htmls[i+2]
                street = street.replace("<td>","")
                street = street.replace("</td>","")
                street = "Rua / Avenida: " + street
        stops.append([reference+"_"+str(points.name),reference+"_"+str(points.name),street,lat,longi,"",""])
    return stops

# Este script le o kml das rotas e as retorna no formato do google transit.
# Nome da Rota, Latitude da parada, Longitude da parada, Sequência
#shapes.txt
def extract_routes(file_name):
    root = parser.fromstring(open(file_name, 'r').read())

    routes = []
    routes.append(["shape_id","shape_pt_lat","shape_pt_lon","shape_pt_sequence"])
    for folder in root.Document.Folder.Folder:
        # coordenadas das paradas
        if (folder.name == "Rotas"):
            for folder2 in folder.Folder:
                for route in folder2.Placemark:
                    coord = route.LineString.coordinates
                    # retira os tabs existentes
                    coord = str(coord).replace("\t","")
                    # retira as quebras de linha existentes
                    coord = str(coord).replace("\n","")
                    output = str(coord).split(" ")
                    #pra cada linha da lista, reorganiza na ordem
                    for line in range(0,len(output)-1):
                        longi,lat,ident = output[line].split(',')
                        route_name = route.name.text[4:].strip() if route.name.text.find("Rota") > -1 else route.name.text
                        route_name = route_name.replace(" ", "_")
                        routes.append([route_name,lat ,longi,str(line + 1)])
    return routes

'''Escreve paradas no formato KML'''
def write_stops(stops,filename,document_name):
    places = []

    for i in range(len(stops)):
        stop = stops[i]
        print i, stop
        place = KML.Placemark(
                      KML.name(str(i) + " " + unicode(stop["stop_id"], errors='ignore')),
                      KML.Point(
                        KML.coordinates(str(stop["stop_lon"]) + "," + str(stop["stop_lat"]) +",0")
                      ),
                      KML.Descrition(unicode(stop["stop_desc"], errors='ignore')),
                      id=str(i)
                    )
        places.append(place)


    document = KML.Document(
            KML.name(document_name),

        )
    document.Placemark = places

    doc = KML.kml(
        document
    )

    file = open(filename, 'w')
    file.write(etree.tostring(doc, pretty_print=True))


#stops = IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT + 'stops.txt')
#print(stops)
#write_stops(stops[:7],"teste.kml")
#if __name__ == '__main__':
 #   routes = extract_routes('/home/celio/Desenvolvimento/bushour/rotas/dados/rotas/Rotas.kml')
 #   IOUtils.save_file_lists(routes, "/home/celio/Desenvolvimento/bushour/rotas/dados/googleTransit/shapesRotas/shapes.txt")
   #print(routes)
#    stops = extract_stops(paths.KML + 'Paradas.kml')
#    print(stops)


