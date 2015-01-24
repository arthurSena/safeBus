#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')

import unittest
from test import test_support

import schedule_interpolator, paths, IOUtils

class Test_schedule_interpolator(unittest.TestCase):

    global list_shapes
    list_shapes = IOUtils.read_file_to_dictlist('../' + paths.GOOGLE_TRANSIT + "shapes.txt")
    global list_stops
    list_stops = IOUtils.read_file_to_dictlist('../' + paths.GOOGLE_TRANSIT + "stops.txt")
    global parada1
    parada1 = {"trip_id":"500_diasUteis_1","arrival_time":"06:30:00","departure_time":"06:30:00","stop_id":"CANTINHO_UNIVERSITARIO_457","stop_sequence":"1","stop_headsign":"","pickup_type":"","shape_dist_traveled":""}
    global parada2
    parada2 = {"trip_id":"500_diasUteis_1","arrival_time":"06:47:00","departure_time":"06:47:00","stop_id":"INTEGRACAO_1","stop_sequence":"2","stop_headsign":"","pickup_type":"","shape_dist_traveled":""}
    global shapes_list
    shapes_list = []
    for shape in list_shapes:
        if (shape["shape_id"] == str(500)):
            shapes_list.append(shape)


    def test_calculatetime(self):
    	self.assertEquals(schedule_interpolator.calculatetime(100,10,0), 10)
    	self.assertEquals(schedule_interpolator.calculatetime(100,10,10), 20)
    	self.assertAlmostEquals(schedule_interpolator.calculatetime(10,3,0), 3.333333, 1)
    	
    	self.assertRaises(ZeroDivisionError,schedule_interpolator.calculatetime,100,0,0)

    def test_calculatespeed(self):
        self.assertAlmostEquals(schedule_interpolator.calculatespeed(parada1,parada2,shapes_list,list_stops), 2661.719279602471/1020,1)


        #duas paradas iguais (horarios iguais)
        self.assertRaises(ZeroDivisionError,schedule_interpolator.calculatespeed,parada1,parada1,shapes_list,list_stops)

        # parada que não existe
        parada3 = {"trip_id":"500_diasUteis_1","arrival_time":"06:47:00","departure_time":"06:47:00","stop_id":"INT","stop_sequence":"2","stop_headsign":"","pickup_type":"","shape_dist_traveled":""}
        self.assertRaises(Exception,schedule_interpolator.calculatespeed,parada1,parada3,shapes_list,list_stops)

        # velocidade negativa
        self.assertRaises(ValueError,schedule_interpolator.calculatespeed,parada2,parada1,shapes_list,list_stops)


    def test_timetoreachsecondpoint(self):
        self.assertAlmostEquals(schedule_interpolator.timetoreachsecondpoint(parada1,parada2,shapes_list,list_stops, 10, 0,500), 267.09,1)

        #duas paradas iguais (horarios iguais)
        self.assertAlmostEquals(schedule_interpolator.timetoreachsecondpoint(parada1,parada1,shapes_list,list_stops, 10, 0,500), 0,1)

        # parada que não existe
        parada3 = {"trip_id":"500_diasUteis_1","arrival_time":"06:47:00","departure_time":"06:47:00","stop_id":"INT","stop_sequence":"2","stop_headsign":"","pickup_type":"","shape_dist_traveled":""}
        self.assertRaises(Exception,schedule_interpolator.timetoreachsecondpoint,parada1,parada3,shapes_list,list_stops, 10, 0,500)

        self.assertAlmostEquals(schedule_interpolator.timetoreachsecondpoint(parada2,parada1,shapes_list,list_stops, 10, 0,500), 858.45753537,1)


    def test_stops_calculate_schedule_interpolator(self):
        stops = [{"stop_id":"CANTINHO_UNIVERSITARIO_457"}, {"stop_id":"FIT_ACADEMIA_560"}, {"stop_id":"CASA_DA_PIZZA_566"}]
        self.assertEquals(schedule_interpolator.stops_calculate_schedule_interpolator(parada1, 10, stops, 500, shapes_list, list_stops), [['06:30:00', 'CANTINHO_UNIVERSITARIO_457'], ['06:30:30', 'FIT_ACADEMIA_560'], ['06:33:54', 'CASA_DA_PIZZA_566']])


        stops1 = [{"stop_id":"CANTINHO_UNIVERSITARIO_457"}]
        self.assertEquals(schedule_interpolator.stops_calculate_schedule_interpolator(parada1, 10, stops1, 500, shapes_list, list_stops), [['06:30:00', 'CANTINHO_UNIVERSITARIO_457']])

        stops2 = [{"stop_id":"CANTINHO_UNIVERSITARIO_457"}, {"stop_id":"INTEGRACAO_1"}]
        self.assertEquals(schedule_interpolator.stops_calculate_schedule_interpolator(parada1, 10, stops2, 500, shapes_list, list_stops), [['06:30:00', 'CANTINHO_UNIVERSITARIO_457'],['06:34:27', 'INTEGRACAO_1']])

        #não tendo parada com horario
        stops3 = [{"stop_id":"FIT_ACADEMIA_560"}, {"stop_id":"CASA_DA_PIZZA_566"}]
        self.assertEquals(schedule_interpolator.stops_calculate_schedule_interpolator(parada1, 10, stops3, 500, shapes_list, list_stops), [['06:30:30', 'FIT_ACADEMIA_560'], ['06:33:54', 'CASA_DA_PIZZA_566']])
        
        #parada com horario ao final(volta completa)
        stops3 = [{"stop_id":"FIT_ACADEMIA_560"}, {"stop_id":"CASA_DA_PIZZA_566"},{"stop_id":"CANTINHO_UNIVERSITARIO_457"}]
        self.assertEquals(schedule_interpolator.stops_calculate_schedule_interpolator(parada1, 10, stops3, 500, shapes_list, list_stops), [['06:30:30', 'FIT_ACADEMIA_560'], ['06:33:54', 'CASA_DA_PIZZA_566'], ['06:48:45', 'CANTINHO_UNIVERSITARIO_457']])
        
        #não tendo paradas
        stops3 = []
        self.assertEquals(schedule_interpolator.stops_calculate_schedule_interpolator(parada1, 10, stops3, 500, shapes_list, list_stops), [])
        

def test_main():
    test_support.run_unittest(Test_schedule_interpolator)

if __name__ == '__main__':
    test_main()
