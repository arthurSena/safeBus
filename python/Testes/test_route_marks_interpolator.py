# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import unittest
from test import test_support

import route_marks_interpolator, IOUtils, paths, routes_manager
from geographiclib.geodesic import Geodesic

class TestaRouteMarksInterpolator(unittest.TestCase):

    def test_put_intermediate_points_on_route(self):
        routes_marks = IOUtils.read_file_to_dictlist("../"+paths.GOOGLE_TRANSIT+"shapes.txt")
        marks_550 = routes_manager.marks_from_route(routes_marks,550)


        route_points = route_marks_interpolator.put_intermediate_points_on_route(10, marks_550)
        for i in range(1, len(route_points)):
            self.assertNotEqual(route_points[i], route_points[i-1])

        #testar com lista de teste
        test_mark = [{'shape_pt_lat': '-7.217149', 'shape_id': '550', 'shape_pt_lon': '-35.911706', 'shape_pt_sequence': '1'}, {'shape_pt_lat': '-7.217276', 'shape_id': '550', 'shape_pt_lon': '-35.910807', 'shape_pt_sequence': '2'}, {'shape_pt_lat': '-7.217305', 'shape_id': '550', 'shape_pt_lon': '-35.910608', 'shape_pt_sequence': '3'}]
        test_points = route_marks_interpolator.put_intermediate_points_on_route(10, test_mark)

        #inicialmente tem 3 pontos. Entre o primeiro e o segundo deve ser adicionado 10 pontos e entre o segundo e o terceiro devem ser adicionados 2 pontos
        self.assertEqual(len(test_points), 15)

        self.assertEqual(float(test_mark[0].get("shape_pt_lat")), float(test_points[0][0]))
        self.assertEqual(float(test_mark[0].get("shape_pt_lon")), float(test_points[0][1]))

        self.assertEqual(float(test_mark[1].get("shape_pt_lat")), float(test_points[11][0]))
        self.assertEqual(float(test_mark[1].get("shape_pt_lon")), float(test_points[11][1]))

        self.assertEqual(float(test_mark[2].get("shape_pt_lat")), float(test_points[14][0]))
        self.assertEqual(float(test_mark[2].get("shape_pt_lon")), float(test_points[14][1]))

        for i in range(1, len(test_points)):
            self.assertNotEqual(test_points[i], test_points[i-1])

        for i in range(1, 12):
            lat1 = test_points[i-1][0]
            lon1 = test_points[i-1][1]
            lat2 = test_points[i][0]
            lon2 = test_points[i][1]
            actual = Geodesic.WGS84.Inverse(float(lat1), float(lon1), float(lat2), float(lon2))["s12"]
            self.assertAlmostEqual(actual, 9, 0)

        for i in range(12, 15):
            lat1 = test_points[i-1][0]
            lon1 = test_points[i-1][1]
            lat2 = test_points[i][0]
            lon2 = test_points[i][1]
            actual = Geodesic.WGS84.Inverse(float(lat1), float(lon1), float(lat2), float(lon2))["s12"]
            self.assertAlmostEqual(actual, 7, 0)

        # Testar com 3 pontos, onde precisa de pontos entre o primeiro e o segundo, mas não entre o segundo e o terceiro
        test_mark = [{'shape_pt_lat': '-7.217149', 'shape_id': '550', 'shape_pt_lon': '-35.911706', 'shape_pt_sequence': '1'}, {'shape_pt_lat': '-7.217276', 'shape_id': '550', 'shape_pt_lon': '-35.910807', 'shape_pt_sequence': '2'}, {'shape_pt_lat': '-7.217305', 'shape_id': '550', 'shape_pt_lon': '-35.910608', 'shape_pt_sequence': '3'}]
        test_points = route_marks_interpolator.put_intermediate_points_on_route(30, test_mark)

        self.assertEqual(len(test_points), 6)

        self.assertEqual(float(test_mark[0].get("shape_pt_lat")), float(test_points[0][0]))
        self.assertEqual(float(test_mark[0].get("shape_pt_lon")), float(test_points[0][1]))

        self.assertEqual(float(test_mark[1].get("shape_pt_lat")), float(test_points[4][0]))
        self.assertEqual(float(test_mark[1].get("shape_pt_lon")), float(test_points[4][1]))

        self.assertEqual(float(test_mark[2].get("shape_pt_lat")), float(test_points[5][0]))
        self.assertEqual(float(test_mark[2].get("shape_pt_lon")), float(test_points[5][1]))

        for i in range(1, len(test_points)):
            self.assertNotEqual(test_points[i], test_points[i-1])

        for i in range(1, 5):
            lat1 = test_points[i-1][0]
            lon1 = test_points[i-1][1]
            lat2 = test_points[i][0]
            lon2 = test_points[i][1]
            actual = Geodesic.WGS84.Inverse(float(lat1), float(lon1), float(lat2), float(lon2))["s12"]
            self.assertAlmostEqual(actual, 25, 0)

        # Testar com 3 pontos, onde não precisa de pontos entre o primeiro e o segundo e precisa entre o segundo e o terceiro
        test_mark = [{'shape_pt_lat': '-7.217305', 'shape_id': '550', 'shape_pt_lon': '-35.910608', 'shape_pt_sequence': '3'}, {'shape_pt_lat': '-7.217276', 'shape_id': '550', 'shape_pt_lon': '-35.910807', 'shape_pt_sequence': '2'},{'shape_pt_lat': '-7.217149', 'shape_id': '550', 'shape_pt_lon': '-35.911706', 'shape_pt_sequence': '1'}]
        test_points = route_marks_interpolator.put_intermediate_points_on_route(30, test_mark)

        self.assertEqual(len(test_points), 6)

        self.assertEqual(float(test_mark[0].get("shape_pt_lat")), float(test_points[0][0]))
        self.assertEqual(float(test_mark[0].get("shape_pt_lon")), float(test_points[0][1]))

        self.assertEqual(float(test_mark[1].get("shape_pt_lat")), float(test_points[1][0]))
        self.assertEqual(float(test_mark[1].get("shape_pt_lon")), float(test_points[1][1]))

        self.assertEqual(float(test_mark[2].get("shape_pt_lat")), float(test_points[5][0]))
        self.assertEqual(float(test_mark[2].get("shape_pt_lon")), float(test_points[5][1]))

        for i in range(1, len(test_points)):
            self.assertNotEqual(test_points[i], test_points[i-1])

        for i in range(2, 6):
            lat1 = test_points[i-1][0]
            lon1 = test_points[i-1][1]
            lat2 = test_points[i][0]
            lon2 = test_points[i][1]
            actual = Geodesic.WGS84.Inverse(float(lat1), float(lon1), float(lat2), float(lon2))["s12"]
            self.assertAlmostEqual(actual, 25, 0)

        # Testar com 3 pontos, onde não precisa de pontos entre o primeiro e o segundo nem entre o segundo e o terceiro
        test_mark = [{'shape_pt_lat': '-7.217305', 'shape_id': '550', 'shape_pt_lon': '-35.910608', 'shape_pt_sequence': '3'}, {'shape_pt_lat': '-7.217276', 'shape_id': '550', 'shape_pt_lon': '-35.910807', 'shape_pt_sequence': '2'},{'shape_pt_lat': '-7.217149', 'shape_id': '550', 'shape_pt_lon': '-35.911706', 'shape_pt_sequence': '1'}]
        test_points = route_marks_interpolator.put_intermediate_points_on_route(200, test_mark)

        self.assertEqual(len(test_points), 3)

        self.assertEqual(float(test_mark[0].get("shape_pt_lat")), float(test_points[0][0]))
        self.assertEqual(float(test_mark[0].get("shape_pt_lon")), float(test_points[0][1]))

        self.assertEqual(float(test_mark[1].get("shape_pt_lat")), float(test_points[1][0]))
        self.assertEqual(float(test_mark[1].get("shape_pt_lon")), float(test_points[1][1]))

        self.assertEqual(float(test_mark[2].get("shape_pt_lat")), float(test_points[2][0]))
        self.assertEqual(float(test_mark[2].get("shape_pt_lon")), float(test_points[2][1]))

        for i in range(1, len(test_points)):
            self.assertNotEqual(test_points[i], test_points[i-1])

        # testar com lista vazia
        test_mark2 = []
        test_points = route_marks_interpolator.put_intermediate_points_on_route(10, test_mark2)
        self.assertEqual(len(test_points), 0)

        # testar se a lista for None
        try:
            test_mark3 = None
            test_points = route_marks_interpolator.put_intermediate_points_on_route(10, test_mark3)
            self.assertTrue(1==0)
        except Exception as e:
            pass

    def test_calculate_number_of_points(self):
        expected1 = 10

        actual1 = route_marks_interpolator.calculate_number_of_points(-7.217149, -35.911706, -7.217276, -35.910807, 10)
        self.assertEqual(actual1, expected1)

        actual2 = route_marks_interpolator.calculate_number_of_points(-7.217276, -35.910807, -7.217149, -35.911706, 10)
        self.assertEqual(actual2, expected1)

        expected2 = 9

        actual3 = route_marks_interpolator.calculate_number_of_points(-7.217149, -35.911706, -7.217248, -35.910874, 10)
        self.assertEqual(actual3, expected2)

        #testa quando distancia minima é um pouco maior que a distancia entre dois pontos
        expected3 = 1
        actual4 = route_marks_interpolator.calculate_number_of_points(-7.217766, -35.907420,-7.217786, -35.907330, 10)
        self.assertEqual(actual4, expected3)


        #testa quando distancia minima é um pouco menor que a distancia entre dois pontos
        expected3 = 0
        actual4 = route_marks_interpolator.calculate_number_of_points(-7.217766, -35.907420,-7.217786, -35.907337, 10)
        self.assertEqual(actual4, expected3)

        #testa quando a distancia minima for 0
        try:
            actual4 = route_marks_interpolator.calculate_number_of_points(-7.217766, -35.907420,-7.217786, -35.907337, 0)
            #deve ir para o except aqui
            self.assertTrue(1 == 0)
        except ZeroDivisionError as e:
            pass

        #testa pontos iguais
        expected3 = 0
        actual5 = route_marks_interpolator.calculate_number_of_points(-7.217766, -35.907420,-7.217766, -35.907420, 1)
        self.assertEqual(actual5, expected3)

        #testa distancia mínima com valor float entre 0 e 1
        expected4 = 20
        actual6 = route_marks_interpolator.calculate_number_of_points(-7.217766, -35.907420,-7.217786, -35.907330, 0.5)
        self.assertEqual(actual6, expected4)


    def test_put_intermediate_points(self):
        intermediate_points = route_marks_interpolator.put_intermediate_points(-7.217149, -35.911706, -7.217276, -35.910807, 10)
        for i in range(1, len(intermediate_points)):
            lat1 = intermediate_points[i-1][0]
            lon1 = intermediate_points[i-1][1]
            lat2 = intermediate_points[i][0]
            lon2 = intermediate_points[i][1]
            actual = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)["s12"]
            self.assertAlmostEqual(actual, 9, 0)

        #testar número de pontos
        self.assertEqual(len(intermediate_points), 10)

    def test_format_transit_points(self):
        routes_marks = IOUtils.read_file_to_dictlist("../"+paths.GOOGLE_TRANSIT+"shapes.txt")
        marks_550 = routes_manager.marks_from_route(routes_marks,550)

        route_points = route_marks_interpolator.format_transit_points(10, marks_550)
        for i in range(1, len(route_points)):
            self.assertNotEqual(route_points[i], route_points[i-1])

        #testar com lista de teste
        test_mark = [{'shape_pt_lat': '-7.217149', 'shape_id': '550', 'shape_pt_lon': '-35.911706', 'shape_pt_sequence': '1'}, {'shape_pt_lat': '-7.217276', 'shape_id': '550', 'shape_pt_lon': '-35.910807', 'shape_pt_sequence': '2'}, {'shape_pt_lat': '-7.217305', 'shape_id': '550', 'shape_pt_lon': '-35.910608', 'shape_pt_sequence': '3'}]
        test_points = route_marks_interpolator.format_transit_points(10, test_mark)

        #inicialmente tem 3 pontos. Entre o primeiro e o segundo deve ser adicionado 10 pontos e entre o segundo e o terceiro devem ser adicionados 2 pontos
        self.assertEqual(len(test_points), 15+1)

        self.assertEqual(float(test_mark[0].get("shape_pt_lat")), float(test_points[1][1]))
        self.assertEqual(float(test_mark[0].get("shape_pt_lon")), float(test_points[1][2]))

        self.assertEqual(float(test_mark[1].get("shape_pt_lat")), float(test_points[12][1]))
        self.assertEqual(float(test_mark[1].get("shape_pt_lon")), float(test_points[12][2]))

        self.assertEqual(float(test_mark[2].get("shape_pt_lat")), float(test_points[15][1]))
        self.assertEqual(float(test_mark[2].get("shape_pt_lon")), float(test_points[15][2]))

        for i in range(1, len(test_points)):
            self.assertNotEqual(test_points[i], test_points[i-1])

        for i in range(2, 13):
            lat1 = test_points[i-1][1]
            lon1 = test_points[i-1][2]
            lat2 = test_points[i][1]
            lon2 = test_points[i][2]
            actual = Geodesic.WGS84.Inverse(float(lat1), float(lon1), float(lat2), float(lon2))["s12"]
            self.assertAlmostEqual(actual, 9, 0)

        for i in range(13, 16):
            lat1 = test_points[i-1][1]
            lon1 = test_points[i-1][2]
            lat2 = test_points[i][1]
            lon2 = test_points[i][2]
            actual = Geodesic.WGS84.Inverse(float(lat1), float(lon1), float(lat2), float(lon2))["s12"]
            self.assertAlmostEqual(actual, 7, 0)

        # testar com lista vazia
        test_mark2 = []
        test_points = route_marks_interpolator.format_transit_points(10, test_mark2)
        self.assertEqual(len(test_points), 1)

        # testar se a lista for None
        try:
            test_mark3 = None
            test_points = route_marks_interpolator.format_transit_points(10, test_mark3)
            self.assertTrue(1==0)
        except Exception as e:
            pass
