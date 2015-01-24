#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')

import unittest
from test import test_support

import stops_from_route, IOUtils, GEOUtils
import paths

class Test_stops_from_route(unittest.TestCase):
    def test_find_stops_routes(self):
        stops = IOUtils.read_file_to_dictlist('../'+ paths.GOOGLE_TRANSIT+'stops.txt')
        marks = IOUtils.read_file_to_dictlist("../" + paths.ROTAS + "shapesRotas/shapes.txt")
        marks_500 = filter(lambda rota: rota.get("shape_id") == "500", marks)

        # Testar se um ponto não é perto de uma parada específica
        mark = [{'shape_pt_lat': '-7.23826', 'shape_id': '004', 'shape_pt_lon': '-35.881541', 'shape_pt_sequence': '2555'}]
        stops = [{'stop_lat': '-7.218956016004086', 'zone_id': '', 'stop_lon': '-35.925779035314918', 'stop_url': '', 'stop_id': '617_-_VIZINHO_881', 'stop_desc': 'Rua / Avenida: VICENTE GOMES DE ALMEIDA', 'stop_name': '617 - VIZINHO_881'}]
        self.assertEqual(len(stops_from_route.find_stops_routes(stops, mark)), 0)

        # Testar se um ponto é perto uma parada específica
        mark = [{'shape_pt_lat': '-7.218913', 'shape_id': '004', 'shape_pt_lon': '-35.925813', 'shape_pt_sequence': '2555'}]
        stops = [{'stop_lat': '-7.218956016004086', 'zone_id': '', 'stop_lon': '-35.925779035314918', 'stop_url': '', 'stop_id': '617_-_VIZINHO_881', 'stop_desc': 'Rua / Avenida: VICENTE GOMES DE ALMEIDA', 'stop_name': '617 - VIZINHO_881'}]

        distance =  GEOUtils.distance2(-7.218913, -35.925813, -7.218956016004086, -35.925779035314918)
        route_stops = stops_from_route.find_stops_routes(stops, mark)
        self.assertEqual(len(route_stops), 1)

        # Testar se stops for uma lista vazia
        mark = [{'shape_pt_lat': '-7.23826', 'shape_id': '004', 'shape_pt_lon': '-35.881541', 'shape_pt_sequence': '2555'}]
        stops = []

        route_stops = stops_from_route.find_stops_routes(stops, mark)
        self.assertEqual(len(route_stops), 0)

        def check_list_equality(l1, l2):
            result = True
            for d1 in l1:
                result = result and (d1 in l2)


            for d2 in l2:
                result = result and (d2 in l1)

            return result

        # Testar quando tenho marcas que passam perto de algumas paradas, se retorna todas as paradas
        stops = [{'stop_lat': '-7.220379011705510', 'zone_id': '', 'stop_lon': '-35.885555036365900', 'stop_url': '', 'stop_id': 'OI_-_TELEMAR_012', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'OI - TELEMAR_012'}, {'stop_lat': '-7.217510975897310', 'zone_id': '', 'stop_lon': '-35.879532974213300', 'stop_url': '', 'stop_id': 'FEIRA_CENTRAL_013', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'FEIRA CENTRAL_013'}, {'stop_lat': '-7.219176962971687', 'zone_id': '', 'stop_lon': '-35.883015990257263', 'stop_url': '', 'stop_id': 'PREFEITURA_094', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PREFEITURA_094'}]
        marks = [{'shape_pt_lat': '-7.22037901170', 'shape_id': '004', 'shape_pt_lon': '-35.88555503636', 'shape_pt_sequence': '2555'}, {'shape_pt_lat': '-7.217490', 'shape_id': '005', 'shape_pt_lon': "-35.879545", 'shape_pt_sequence': '2556'}, {'shape_pt_lat': '-7.219140', 'shape_id': '006', 'shape_pt_lon': '-35.883038', 'shape_pt_sequence': '2556'}]
        route_stops = stops_from_route.find_stops_routes(stops, marks)

        self.assertTrue(check_list_equality(route_stops, stops))

        # Testar quando tenho marcas que não passam perto de algumas paradas, se retorna uma lista de paradas vazia
        stops = [{'stop_lat': '-7.220379011705510', 'zone_id': '', 'stop_lon': '-35.885555036365900', 'stop_url': '', 'stop_id': 'OI_-_TELEMAR_012', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'OI - TELEMAR_012'}, {'stop_lat': '-7.217510975897310', 'zone_id': '', 'stop_lon': '-35.879532974213300', 'stop_url': '', 'stop_id': 'FEIRA_CENTRAL_013', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'FEIRA CENTRAL_013'}, {'stop_lat': '-7.219176962971687', 'zone_id': '', 'stop_lon': '-35.883015990257263', 'stop_url': '', 'stop_id': 'PREFEITURA_094', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PREFEITURA_094'}]
        marks = [{'shape_pt_lat': '-9.22037901170', 'shape_id': '004', 'shape_pt_lon': '-35.88555503636', 'shape_pt_sequence': '2555'}, {'shape_pt_lat': '-9.217490', 'shape_id': '005', 'shape_pt_lon': "-35.879545", 'shape_pt_sequence': '2556'}, {'shape_pt_lat': '-9.219140', 'shape_id': '006', 'shape_pt_lon': '-35.883038', 'shape_pt_sequence': '2556'}]
        route_stops = stops_from_route.find_stops_routes(stops, marks)

        self.assertListEqual(route_stops, [])

        # Testar quando tenho marcas que tanto passam perto de algumas paradas quando que não passam, se retorna uma lista apenas com as paradas perto
        stops = [{'stop_lat': '-7.220379011705510', 'zone_id': '', 'stop_lon': '-35.885555036365900', 'stop_url': '', 'stop_id': 'OI_-_TELEMAR_012', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'OI - TELEMAR_012'}, {'stop_lat': '-7.217510975897310', 'zone_id': '', 'stop_lon': '-35.879532974213300', 'stop_url': '', 'stop_id': 'FEIRA_CENTRAL_013', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'FEIRA CENTRAL_013'}, {'stop_lat': '-7.219176962971687', 'zone_id': '', 'stop_lon': '-35.883015990257263', 'stop_url': '', 'stop_id': 'PREFEITURA_094', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PREFEITURA_094'}]
        marks = [{'shape_pt_lat': '-9.22037901170', 'shape_id': '004', 'shape_pt_lon': '-35.88555503636', 'shape_pt_sequence': '2555'}, {'shape_pt_lat': '-7.217490', 'shape_id': '005', 'shape_pt_lon': "-35.879545", 'shape_pt_sequence': '2556'}, {'shape_pt_lat': '-7.219140', 'shape_id': '006', 'shape_pt_lon': '-35.883038', 'shape_pt_sequence': '2556'}]
        route_stops = stops_from_route.find_stops_routes(stops, marks)
        expected_stops = [{'stop_lat': '-7.217510975897310', 'zone_id': '', 'stop_lon': '-35.879532974213300', 'stop_url': '', 'stop_id': 'FEIRA_CENTRAL_013', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'FEIRA CENTRAL_013'}, {'stop_lat': '-7.219176962971687', 'zone_id': '', 'stop_lon': '-35.883015990257263', 'stop_url': '', 'stop_id': 'PREFEITURA_094', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PREFEITURA_094'}]
        self.assertTrue(check_list_equality(route_stops, expected_stops))

    def test_get_stops_nearby(self):
        # Testar se um ponto não é perto de uma parada específica
        mark = {'shape_pt_lat': '-7.23826', 'shape_id': '004', 'shape_pt_lon': '-35.881541', 'shape_pt_sequence': '2555'}
        stops = [{'stop_lat': '-7.218956016004086', 'zone_id': '', 'stop_lon': '-35.925779035314918', 'stop_url': '', 'stop_id': '617_-_VIZINHO_881', 'stop_desc': 'Rua / Avenida: VICENTE GOMES DE ALMEIDA', 'stop_name': '617 - VIZINHO_881'}]
        self.assertEqual(len(stops_from_route.get_stops_nearby(mark, stops)), 0)

        # Testar se um ponto é perto uma parada específica
        mark = {'shape_pt_lat': '-7.218913', 'shape_id': '004', 'shape_pt_lon': '-35.925813', 'shape_pt_sequence': '2555'}
        stops = [{'stop_lat': '-7.218956016004086', 'zone_id': '', 'stop_lon': '-35.925779035314918', 'stop_url': '', 'stop_id': '617_-_VIZINHO_881', 'stop_desc': 'Rua / Avenida: VICENTE GOMES DE ALMEIDA', 'stop_name': '617 - VIZINHO_881'}]

        distance =  GEOUtils.distance2(-7.218913, -35.925813, -7.218956016004086, -35.925779035314918)
        stops_nearby = stops_from_route.get_stops_nearby(mark, stops)
        self.assertEqual(len(stops_nearby), 1)
        self.assertEqual(stops_nearby[0][1], distance)

        # Testar se vem ordenado por distancia
        stops = [{'stop_lat': '-7.220379011705510', 'zone_id': '', 'stop_lon': '-35.885555036365900', 'stop_url': '', 'stop_id': 'OI_-_TELEMAR_012', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'OI - TELEMAR_012'}, {'stop_lat': '-7.217510975897310', 'zone_id': '', 'stop_lon': '-35.879532974213300', 'stop_url': '', 'stop_id': 'FEIRA_CENTRAL_013', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'FEIRA CENTRAL_013'}, {'stop_lat': '-7.219176962971687', 'zone_id': '', 'stop_lon': '-35.883015990257263', 'stop_url': '', 'stop_id': 'PREFEITURA_094', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PREFEITURA_094'}, {'stop_lat': '-7.218267023563385', 'zone_id': '', 'stop_lon': '-35.88107499293983', 'stop_url': '', 'stop_id': 'PAGUE_FACIL_097', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PAGUE FACIL_097'}, {'stop_lat': '-7.21808304078877', 'zone_id': '', 'stop_lon': '-35.880768969655037', 'stop_url': '', 'stop_id': 'REDE_COMPRAS_098', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'REDE COMPRAS_098'}, {'stop_lat': '-7.217688001692295', 'zone_id': '', 'stop_lon': '-35.879819970577955', 'stop_url': '', 'stop_id': '1044_099', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1044_099'}, {'stop_lat': '-7.217594962567091', 'zone_id': '', 'stop_lon': '-35.879602041095495', 'stop_url': '', 'stop_id': '1054_100', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1054_100'}, {'stop_lat': '-7.215876001864672', 'zone_id': '', 'stop_lon': '-35.876044007018209', 'stop_url': '', 'stop_id': '1520_101', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1520_101'}, {'stop_lat': '-7.21451997756958', 'zone_id': '', 'stop_lon': '-35.873102964833379', 'stop_url': '', 'stop_id': '1834_102', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1834_102'}, {'stop_lat': '-7.214802028611302', 'zone_id': '', 'stop_lon': '-35.874166963621974', 'stop_url': '', 'stop_id': '1726_-_OPOSTO_103', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1726 - OPOSTO_103'}, {'stop_lat': '-7.21587298437953', 'zone_id': '', 'stop_lon': '-35.876393029466271', 'stop_url': '', 'stop_id': '1461_104', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1461_104'}, {'stop_lat': '-7.219114014878869', 'zone_id': '', 'stop_lon': '-35.883358977735043', 'stop_url': '', 'stop_id': 'JUIZADO_DO_CONSUMIDOR_105', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'JUIZADO DO CONSUMIDOR_105'}, {'stop_lat': '-7.220322014763951', 'zone_id': '', 'stop_lon': '-35.885846978053451', 'stop_url': '', 'stop_id': 'DAMAS_106', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'DAMAS_106'}, {'stop_lat': '-7.22042603418231', 'zone_id': '', 'stop_lon': '-35.886013023555279', 'stop_url': '', 'stop_id': '289E_108', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '289E_108'}, {'stop_lat': '-7.223939979448915', 'zone_id': '', 'stop_lon': '-35.893642986193299', 'stop_url': '', 'stop_id': 'REAL_CLUBE_109', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'REAL CLUBE_109'}, {'stop_lat': '-7.226473996415734', 'zone_id': '', 'stop_lon': '-35.899007990956306', 'stop_url': '', 'stop_id': 'HELENO_CABELEREIRO_110', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'HELENO CABELEREIRO_110'}, {'stop_lat': '-7.228187005966902', 'zone_id': '', 'stop_lon': '-35.902856038883328', 'stop_url': '', 'stop_id': '1640_111', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1640_111'}, {'stop_lat': '-7.230028007179499', 'zone_id': '', 'stop_lon': '-35.907143969088793', 'stop_url': '', 'stop_id': 'MULTI_CAR_-_OPOSTO_112', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'MULTI CAR - OPOSTO_112'}, {'stop_lat': '-7.23089100793004', 'zone_id': '', 'stop_lon': '-35.909094018861651', 'stop_url': '', 'stop_id': '2380_113', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '2380_113'}, {'stop_lat': '-7.233152026310563', 'zone_id': '', 'stop_lon': '-35.914154006168246', 'stop_url': '', 'stop_id': 'VERBO_DA_VIDA_-_OPOSTO_114', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'VERBO DA VIDA - OPOSTO_114'}, {'stop_lat': '-7.234217030927539', 'zone_id': '', 'stop_lon': '-35.916621973738074', 'stop_url': '', 'stop_id': 'IGREJA_EVANGELICA_115', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'IGREJA EVANGELICA_115'}, {'stop_lat': '-7.234845003113151', 'zone_id': '', 'stop_lon': '-35.918043041601777', 'stop_url': '', 'stop_id': 'MAXXI_ATACADO_116', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'MAXXI ATACADO_116'}, {'stop_lat': '-7.23682296462357', 'zone_id': '', 'stop_lon': '-35.922676976770163', 'stop_url': '', 'stop_id': '4060_117', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '4060_117'}, {'stop_lat': '-7.238340005278587', 'zone_id': '', 'stop_lon': '-35.926131997257471', 'stop_url': '', 'stop_id': '4130_118', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '4130_118'}, {'stop_lat': '-7.238983986899257', 'zone_id': '', 'stop_lon': '-35.92765599489212', 'stop_url': '', 'stop_id': 'BAR_SURUBIM_-_OPOSTO_119', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'BAR SURUBIM - OPOSTO_119'}, {'stop_lat': '-7.240465991199017', 'zone_id': '', 'stop_lon': '-35.931123001500964', 'stop_url': '', 'stop_id': 'HOSPITAL_DE_TRAUMA_120', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'HOSPITAL DE TRAUMA_120'}, {'stop_lat': '-7.239194037392736', 'zone_id': '', 'stop_lon': '-35.927593968808651', 'stop_url': '', 'stop_id': 'BAR_SURUBIM_122', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'BAR SURUBIM_122'}, {'stop_lat': '-7.238525999709964', 'zone_id': '', 'stop_lon': '-35.926066031679511', 'stop_url': '', 'stop_id': '17_123', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '17_123'}, {'stop_lat': '-7.237103004008532', 'zone_id': '', 'stop_lon': '-35.922850985080004', 'stop_url': '', 'stop_id': '08_124', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '08_124'}, {'stop_lat': '-7.236501015722752', 'zone_id': '', 'stop_lon': '-35.921370992437005', 'stop_url': '', 'stop_id': '14B_125', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '14B_125'}, {'stop_lat': '-7.235221015289426', 'zone_id': '', 'stop_lon': '-35.918448977172375', 'stop_url': '', 'stop_id': 'MEGA_NORDESTE_126', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'MEGA NORDESTE_126'}, {'stop_lat': '-7.233501970767975', 'zone_id': '', 'stop_lon': '-35.914534041658044', 'stop_url': '', 'stop_id': 'FAVELA_DO_PAPELAO_127', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'FAVELA DO PAPELAO_127'}, {'stop_lat': '-7.232992015779018', 'zone_id': '', 'stop_lon': '-35.913394019007683', 'stop_url': '', 'stop_id': 'RHEMA_128', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'RHEMA_128'}, {'stop_lat': '-7.232174025848508', 'zone_id': '', 'stop_lon': '-35.91156299225986', 'stop_url': '', 'stop_id': '2693_129', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '2693_129'}, {'stop_lat': '-7.231200970709324', 'zone_id': '', 'stop_lon': '-35.909317983314395', 'stop_url': '', 'stop_id': 'PIZZARELLA_-_OPOSTO_130', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PIZZARELLA - OPOSTO_130'}, {'stop_lat': '-7.230352973565459', 'zone_id': '', 'stop_lon': '-35.907427025958896', 'stop_url': '', 'stop_id': 'MULTICAR_131', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'MULTICAR_131'}, {'stop_lat': '-7.22904103808105', 'zone_id': '', 'stop_lon': '-35.90451599098742', 'stop_url': '', 'stop_id': '1819_132', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1819_132'}, {'stop_lat': '-7.228791005909443', 'zone_id': '', 'stop_lon': '-35.904309041798115', 'stop_url': '', 'stop_id': '1800_133', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1800_133'}, {'stop_lat': '-7.227765982970595', 'zone_id': '', 'stop_lon': '-35.901462966576219', 'stop_url': '', 'stop_id': '1359_135', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1359_135'}, {'stop_lat': '-7.226698966696858', 'zone_id': '', 'stop_lon': '-35.899073034524918', 'stop_url': '', 'stop_id': 'IGREJA_SAO_CRISTOVAO_136', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'IGREJA SAO CRISTOVAO_136'}, {'stop_lat': '-7.225063992664218', 'zone_id': '', 'stop_lon': '-35.895604016259313', 'stop_url': '', 'stop_id': 'APTA_-_OPOSTO_137', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'APTA - OPOSTO_137'}, {'stop_lat': '-7.2238630335778', 'zone_id': '', 'stop_lon': '-35.893097994849086', 'stop_url': '', 'stop_id': '845_138', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '845_138'}, {'stop_lat': '-7.21965498290956', 'zone_id': '', 'stop_lon': '-35.88401997461915', 'stop_url': '', 'stop_id': 'PRACA_CLEMENTINO_PROCOPIO_140', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PRACA CLEMENTINO PROCOPIO_140'}, {'stop_lat': '-7.218091003596783', 'zone_id': '', 'stop_lon': '-35.881127966567874', 'stop_url': '', 'stop_id': 'BOMPRECO_143', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'BOMPRECO_143'}, {'stop_lat': '-7.218154035508633', 'zone_id': '', 'stop_lon': '-35.88124799542129', 'stop_url': '', 'stop_id': 'BOMPRECO_144', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'BOMPRECO_144'}, {'stop_lat': '-7.218463998287916', 'zone_id': '', 'stop_lon': '-35.881946040317416', 'stop_url': '', 'stop_id': 'ARCA_CATEDRAL_145', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'ARCA CATEDRAL_145'}, {'stop_lat': '-7.218560976907611', 'zone_id': '', 'stop_lon': '-35.88219297118485', 'stop_url': '', 'stop_id': 'ANTIGO_PHD_146', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'ANTIGO PHD_146'}, {'stop_lat': '-7.21973704174161', 'zone_id': '', 'stop_lon': '-35.884739980101585', 'stop_url': '', 'stop_id': 'PRACA_DA_BANDEIRA_147', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PRACA DA BANDEIRA_147'}, {'stop_lat': '-7.219895962625742', 'zone_id': '', 'stop_lon': '-35.885014990344644', 'stop_url': '', 'stop_id': 'PRACA_DA_BANDEIRA_149', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PRACA DA BANDEIRA_149'}, {'stop_lat': '-7.220155969262123', 'zone_id': '', 'stop_lon': '-35.885573979467154', 'stop_url': '', 'stop_id': 'DAMAS_151', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'DAMAS_151'}, {'stop_lat': '-7.220550002530217', 'zone_id': '', 'stop_lon': '-35.88642499409616', 'stop_url': '', 'stop_id': 'JR_CABELEREIRO_152', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'JR CABELEREIRO_152'}, {'stop_lat': '-7.227328028529882', 'zone_id': '', 'stop_lon': '-35.901032974943519', 'stop_url': '', 'stop_id': '1328_153', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': '1328_153'}, {'stop_lat': '-7.23104196600616', 'zone_id': '', 'stop_lon': '-35.909395013004541', 'stop_url': '', 'stop_id': 'PIZZARELLA_154', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'PIZZARELLA_154'}, {'stop_lat': '-7.220496023073793', 'zone_id': '', 'stop_lon': '-35.885902969166636', 'stop_url': '', 'stop_id': 'ARCA_TITAO_155', 'stop_desc': 'Rua / Avenida: FLORIANO PEIXOTO', 'stop_name': 'ARCA TITAO_155'}]
        mark = {'shape_pt_lat': '-7.218091003596783', 'shape_id': '004', 'shape_pt_lon': '-35.881127966567874', 'shape_pt_sequence': '2555'}

        check_ordered = lambda list, i: True if i >= (len(list) - 1) else list[i][1] < list[i+1][1] and check_ordered(list, i + 1)
        stops_nearby = stops_from_route.get_stops_nearby(mark, stops)

        self.assertTrue(check_ordered(stops_nearby, 0))

        # Testar se stops for uma lista vazia
        mark = {'shape_pt_lat': '-7.23826', 'shape_id': '004', 'shape_pt_lon': '-35.881541', 'shape_pt_sequence': '2555'}
        stops = []

        stops_nearby = stops_from_route.get_stops_nearby(mark, stops)
        self.assertEqual(len(stops_nearby), 0)




def test_main():
    test_support.run_unittest(Test_stops_from_route)

if __name__ == '__main__':
    test_main()
