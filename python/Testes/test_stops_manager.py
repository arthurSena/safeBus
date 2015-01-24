# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import unittest
from test import test_support

import stops_manager,IOUtils, paths
from test import test_support


class Test_stops_manager(unittest.TestCase):



    def test_stops_distance(self):
        list_stops = IOUtils.read_file_to_dictlist("documentosTeste/stops_test.txt")
        routes_marks = IOUtils.read_file_to_dictlist("documentosTeste/shapes_test.txt")
        first_stop= list_stops[0]
        last_stop = list_stops[2]
        route_id = "00"
        first = None
        distance = (stops_manager.stops_distance(first_stop, last_stop, route_id, routes_marks,list_stops))
        #self.assertAlmostEqual(distance, 200, 0)

    def test_stop_coordinates(self):
        # Testa quando uma parada esta na lista de paradas
        stops = [{'stop_lat': '-7.221078984439373', 'zone_id': '', 'stop_lon': '-35.874209962785244', 'stop_url': '', 'stop_id': '70_001', 'stop_desc': 'Rua / Avenida: CAMPOS SALES', 'stop_name': '70_001'},
                 {'stop_lat': '-7.222693003714085', 'zone_id': '', 'stop_lon': '-35.873241014778614', 'stop_url': '', 'stop_id': '274_002', 'stop_desc': 'Rua / Avenida: CAMPOS SALES', 'stop_name': '274_002'},
                 {'stop_lat': '-7.226035036146641', 'zone_id': '', 'stop_lon': '-35.873269010335207', 'stop_url': '', 'stop_id': '449_003', 'stop_desc': 'Rua / Avenida: FERNANDES VIEIRA', 'stop_name': '449_003'}]

        coordinate = stops_manager.stop_coordinates("70_001", stops)
        self.assertDictEqual({"lat": -7.221078984439373,"lon":-35.874209962785244}, coordinate)

        coordinate2 = stops_manager.stop_coordinates("274_002", stops)
        self.assertDictEqual({"lat": -7.222693003714085,"lon":-35.873241014778614}, coordinate2)

        # Testa quando uma parada não esta na lista de paradas
        stops = [{'stop_lat': '-7.221078984439373', 'zone_id': '', 'stop_lon': '-35.874209962785244', 'stop_url': '', 'stop_id': '70_001', 'stop_desc': 'Rua / Avenida: CAMPOS SALES', 'stop_name': '70_001'},
                 {'stop_lat': '-7.222693003714085', 'zone_id': '', 'stop_lon': '-35.873241014778614', 'stop_url': '', 'stop_id': '274_002', 'stop_desc': 'Rua / Avenida: CAMPOS SALES', 'stop_name': '274_002'},
                 {'stop_lat': '-7.226035036146641', 'zone_id': '', 'stop_lon': '-35.873269010335207', 'stop_url': '', 'stop_id': '449_003', 'stop_desc': 'Rua / Avenida: FERNANDES VIEIRA', 'stop_name': '449_003'}]
        coordinate = stops_manager.stop_coordinates("654654", stops)

        self.assertEqual(None, coordinate)

        # Testa quando a lista de paradas é vazia
        stops = []
        coordinate = stops_manager.stop_coordinates("654654", stops)

        self.assertEqual(None, coordinate)

        # Testa quando uma lista de paradas não tem a chave "stop_id"
        stops = [{'stop_lat': '-7.221078984439373', 'zone_id': '', 'stop_lon': '-35.874209962785244', 'stop_url': '', 'stop_desc': 'Rua / Avenida: CAMPOS SALES', 'stop_name': '70_001'}]
        try:
            coordinate = stops_manager.stop_coordinates("654654", stops)
            self.assertEqual(1,0)
        except:
            pass

    def test_closest_mark_from_stop(self):

        coord = {"lat": '-7.244805',"lon":-35.906694}
        shape_list = IOUtils.read_file_to_dictlist("documentosTeste/shapes_test.txt")
        #closer_coord =  (-7.244811, -35.906761)

        self.assertEqual(stops_manager.closest_mark_from_stop(coord,shape_list), 7)

        shape_aux_list1 = None
        self.assertIsNone(stops_manager.closest_mark_from_stop(coord,shape_aux_list1))

        coord1 = None
        self.assertIsNone(stops_manager.closest_mark_from_stop(coord1,shape_list))

        coord_aux = {}
        self.assertIsNone(stops_manager.closest_mark_from_stop(coord_aux,shape_list))

        shape_aux_list = []
        self.assertIsNone(stops_manager.closest_mark_from_stop(coord,shape_aux_list))

        self.assertIsNone(stops_manager.closest_mark_from_stop(coord_aux,shape_aux_list))



    def test_repeated_points(self):
        list_stops = IOUtils.read_file_to_dictlist("documentosTeste/stops_test.txt")
        repetidas = stops_manager.repeated_points(list_stops)
        self.assertEquals( 'ID_TEST', repetidas[0][0]["stop_id"])

def test_main():
    test_support.run_unittest(Test_stops_manager)

if __name__ == '__main__':
    test_main()

