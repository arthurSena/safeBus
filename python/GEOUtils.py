#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import UnityUtils
from geographiclib.geodesic import Geodesic

# Calcula a distancia entre dois pontos dados
distances = {}
def distance(lat1,lon1,lat2,lon2):
    if lon1 < -180 or lon1 > 180:
        raise ValueError('latitude %f not in [-180, 180]' % (lon1))
    if lon2 < -180 or lon2 > 180:
        raise ValueError('latitude %f not in [-180, 180]' % (lon2))

    g = Geodesic.WGS84.Inverse(float(lat1), float(lon1), float(lat2), float(lon2))
    return g['s12']

def distance2(lat1, lon1,lat2, lon2, el1 = 0, el2 = 0):
    if(distances.has_key((lat1,lon1,lat2,lon2))):
        return distances[(lat1,lon1,lat2,lon2)]
    elif (distances.has_key((lat2,lon2,lat1,lon1))):
        return distances[(lat2,lon2,lat1,lon1)]

    lat1, lon1,lat2, lon2 = float(lat1), float(lon1),float(lat2), float(lon2)
    R = 6371 # Radius of the earth
    latDistance = UnityUtils.deg2rad(lat2 - lat1)
    lonDistance = UnityUtils.deg2rad(lon2 - lon1)
    a = math.sin(latDistance / 2) * math.sin(latDistance / 2) + math.cos(UnityUtils.deg2rad(lat1)) * math.cos(UnityUtils.deg2rad(lat2)) * math.sin(lonDistance / 2) * math.sin(lonDistance / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 1000 # convert to meters
    height = el1 - el2
    distance = math.pow(distance, 2) + math.pow(height, 2)
    distance = math.sqrt(distance)
    distances[(lat1,lon1,lat2,lon2)] = distance
    return distance

#verifica a direção de dado ponto (lat3, lon3) em relação a reta (lat1, lon1, lat2, lon2) 
#retorna negativo se estiver no sentido contrario, positivo se estiver o mesmo sentido e 0 (zero) se estiver no mesmo ponto
def check_direction(lat1,lon1,lat2,lon2,lat3,lon3):
    direction = (lat2 - lat1) * (lon3 - lon1) - (lon2 - lon1) * (lat3 - lat1)
    return direction