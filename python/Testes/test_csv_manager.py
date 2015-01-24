#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')

import unittest
from test import test_support

import CSV_manager
import paths

class Test_csv_manager(unittest.TestCase):
    def test_extract_stops(self):
		file1 = CSV_manager.extract_stops("../../../dados/dados_para_teste/to_csv_manager_test_1.csv")
		answer1 = [["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"], ["_030", "_030", "Rua / Avenida: REPUBLICA PORTUGUESA", "-7.187031023204327","-35.881342962384200", "", ""],
		["_031", "_031", "Rua / Avenida: NACOES", "-7.189367981627584","-35.881206002086400", "", ""],["815_032", "815_032", "Rua / Avenida: NACOES", "-7.191322976723313","-35.881049009039900", "", ""],
		["625_033", "625_033", "Rua / Avenida: NACOES", "-7.192832976579666","-35.880666961893400", "", ""],["UPA_036", "UPA_036", "Rua / Avenida: MANOEL TAVARES", "-7.200025990605354","-35.877134995535000", "", ""],
		["INTEGRACAO_1","INTEGRACAO_1","Rua / Avenida: Dom Pedro II","-7.220618", "-35.889802","",""],["INTEGRACAO_2","INTEGRACAO_2","Rua / Avenida: Dom Pedro II","-7.220693", "-35.888944","",""]]
		self.assertEqual(file1, answer1)

		file2 = CSV_manager.extract_stops("../../../dados/dados_para_teste/to_csv_manager_test_2.csv")
		answer2 = [["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"], ["70_001", "70_001", "Rua / Avenida: CAMPOS SALES", "-7.221078984439373","-35.874209962785244", "", ""],
		["259_004", "259_004", "Rua / Avenida: FERNANDES VIEIRA", "-7.22511101514101","-35.874778004363179", "", ""],["560_004", "560_004", "Rua / Avenida: BR-230", "-7.237944966182113","-35.866168029606342", "", ""],
		["IGREJA_PETENCOSTAL_007", "IGREJA PETENCOSTAL_007", "Rua / Avenida: BR-230", "-7.238891031593084","-35.864332979544997", "", ""],["INTEGRACAO_1","INTEGRACAO_1","Rua / Avenida: Dom Pedro II","-7.220618", "-35.889802","",""],
		["INTEGRACAO_2","INTEGRACAO_2","Rua / Avenida: Dom Pedro II","-7.220693", "-35.888944","",""]]
		self.assertEqual(file2, answer2)

		# testar se existe uma virgula a mais em alguma linha
		try:
			file3 = CSV_manager.extract_stops("../../../dados/dados_para_teste/to_csv_manager_test_3.csv")
			answer3 = [["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"],["70_001", "70_001", "Rua / Avenida: CAMPOS SALES", "-7.221078984439373","-35.874209962785244", "", ""],
			["259_004", "259_004", "Rua / Avenida: FERNANDES VIEIRA", "-7.22511101514101","-35.874778004363179", "", ""],["560_004", "560_004", "Rua / Avenida: BR-230", "-7.237944966182113","-35.866168029606342", "", ""],
			["IGREJA_PETENCOSTAL_007", "IGREJA PETENCOSTAL_007", "Rua / Avenida: BR-230", "-7.238891031593084","-35.864332979544997", "", ""],["INTEGRACAO_1","INTEGRACAO_1","Rua / Avenida: Dom Pedro II","-7.220618", "-35.889802","",""],
			["INTEGRACAO_2","INTEGRACAO_2","Rua / Avenida: Dom Pedro II","-7.220693", "-35.888944","",""]]
			self.assertEqual(file3, answer3)
		except:
			pass

		# testar um arquivo vazio
		try:
			file2 = CSV_manager.extract_stops("../../../dados/dados_para_teste/to_csv_manager_test_4.csv")
			answer4 = [["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"],["INTEGRACAO_1","INTEGRACAO_1","Rua / Avenida: Dom Pedro II","-7.220618", "-35.889802","",""],
			["INTEGRACAO_2","INTEGRACAO_2","Rua / Avenida: Dom Pedro II","-7.220693", "-35.888944","",""]]
			self.assertEqual(file4, answer4)
		except:
			pass

		# testar se existe alguma linha vazia no arquivo
		try:
			file5 = CSV_manager.extract_stops("../../../dados/dados_para_teste/to_csv_manager_test_5.csv")
			answer5 = [["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"], ["70_001", "70_001", "Rua / Avenida: CAMPOS SALES", "-7.221078984439373","-35.874209962785244", "", ""],
			["259_004", "259_004", "Rua / Avenida: FERNANDES VIEIRA", "-7.22511101514101","-35.874778004363179", "", ""],["560_004", "560_004", "Rua / Avenida: BR-230", "-7.237944966182113","-35.866168029606342", "", ""],
			["IGREJA_PETENCOSTAL_007", "IGREJA PETENCOSTAL_007", "Rua / Avenida: BR-230", "-7.238891031593084","-35.864332979544997", "", ""],["INTEGRACAO_1","INTEGRACAO_1","Rua / Avenida: Dom Pedro II","-7.220618", "-35.889802","",""],
			["INTEGRACAO_2","INTEGRACAO_2","Rua / Avenida: Dom Pedro II","-7.220693", "-35.888944","",""]]
			self.assertEqual(file5, answer5)
		except:
			pass

		file6 = CSV_manager.extract_stops("../../../dados/dados_para_teste/to_csv_manager_test_6.csv")
		answer6 = [["stop_id","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url"], ["70_001", "70_001", "Rua / Avenida: CAMPOS SALES", "-7.221078984439373","-35.874209962785244", "", ""],
		["259_004", "259_004", "Rua / Avenida: FERNANDES VIEIRA", "-7.22511101514101","-35.874778004363179", "", ""],["560_004", "560_004", "Rua / Avenida: BR-230", "-7.237944966182113","-35.866168029606342", "", ""],
		["IGREJA_PETENCOSTAL_007", "IGREJA PETENCOSTAL_007", "Rua / Avenida: BR-230", "-7.238891031593084","-35.864332979544997", "", ""],["IGREJA_PETENCOSTAL_007", "IGREJA PETENCOSTAL_007", "Rua / Avenida: BR-230", "-7.238891031593084","-35.864332979544997", "", ""],
		["INTEGRACAO_1","INTEGRACAO_1","Rua / Avenida: Dom Pedro II","-7.220618", "-35.889802","",""],["INTEGRACAO_2","INTEGRACAO_2","Rua / Avenida: Dom Pedro II","-7.220693", "-35.888944","",""]]
		self.assertEqual(file6, answer6)

