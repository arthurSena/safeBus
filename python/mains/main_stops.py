#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')

import IOUtils, paths, CSV_manager

if __name__ == '__main__':
    stops = CSV_manager.extract_stops("../"+paths.PARADAS_SEM_REPETICAO+"paradas_rotas_original.csv")
    IOUtils.save_file_lists(stops,"../"+paths.GOOGLE_TRANSIT+ "stops.txt")